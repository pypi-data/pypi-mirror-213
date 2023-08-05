from loguru import logger as log
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
from random import choice
from orbit_database import Doc
from datetime import datetime
from orbit_component_base.schema.OrbitUsers import UsersCollection, UsersTable
from orbit_component_base.schema.OrbitSessions import SessionsTable
from orbit_component_base.src.orbit_shared import world


class OrbitAuth:

    CHARACTERS = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    CODE_SIZE = 8
    EXPIRY_TIME = 3600
    _keyPair = None

    def __init__(self, sid, ns):
        self._sid = sid
        self._ns = ns
        if not self._keyPair:
            self.__class__._keyPair = RSA.generate(2048)

    def generate_auth_code(self):
        code = ''
        for i in range(self.CODE_SIZE):
            code += choice(self.CHARACTERS)
        return code

    def activate_user(self, user):
        user.update({'active': True, 'code': None}).save()
        return {'ok': True, 'validate': False}

    def activate_session (self, user_id, auth, session):
        SessionsTable().from_doc(Doc({
            'user_id'   : user_id,
            'when'      : datetime.now().timestamp(),
            'vendor'    : auth.get('vendor', 'unknown'),
            'platform'  : auth.get('platform', 'unknown'),
            'language'  : auth.get('language', 'unknown'),
            'address'   : session['address'],
            'host_id'   : session['host_id'],
            'sid'       : self._sid,
            'ns'        : self._ns
        })).append()

    async def confirm(self, auth, get_session, save_session):
        session = await get_session(self._sid)
        try:
            host_id = auth.get('host_id')
            if host_id != session['host_id']:
                return {'ok': False, 'error': f'No such hostId: {host_id}'}
            user = UsersTable().from_key(host_id)
            if not user.isValid:
                return {'ok': False, 'error': f'no such user: {host_id}'}

            cipher = PKCS1_OAEP.new(self._keyPair, SHA256)
            ciphertext = cipher.decrypt(b64decode(auth.get('user_id'))).decode()
            if user._user_id != ciphertext:
                return {'ok': False, 'error': 'bad cipher text'}
            if user._active:
                return {'ok': False, 'error': 'user already activated'}
            if datetime.now().timestamp() - user._when > self.EXPIRY_TIME:
                return {'ok': False, 'error': 'activation code has expired'}
            if user._tries > 3:
                return {'ok': False, 'error': 'too many attempts, activation code expired'}

            code = auth.get('code_id')
            ciphertext = cipher.decrypt(b64decode(code)).decode()

            if user._code != ciphertext:
                user._tries += 1
                user.save()
                log.error(f'bad activation code supplier: {ciphertext}')
                return {'ok': False, 'error': 'bad activation code'}
            self.activate_session(user._user_id, auth, session)
            return self.activate_user(user)
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}

    async def validate(self, auth, get_session, save_session):
        session = await get_session(self._sid)
        try:
            host_id = auth.get('host_id')
            secret = auth.get('secret')
            if host_id != session['host_id']:
                return {'ok': False, 'error': f'No such hostId: {host_id}'}
            cipher = PKCS1_OAEP.new(self._keyPair, SHA256)
            user_id = cipher.decrypt(b64decode(secret)).decode()
            user = UsersTable().from_key(host_id)
            if user.isValid:
                if user._user_id == user_id:
                    if user._active or world.conf.authentication == 'autoenroll':
                        session['activated'] = True
                        session['perm'] = user._perm
                        log.debug(f'Save: {self._sid} / {self._ns} => {session}')
                        try:
                            await save_session(self._sid, session)
                            self.activate_session(user._user_id, auth, session)
                        except Exception as e:
                            log.error(e)
                            
                        return {'ok': True, 'validate': False}
                    return {'ok': True, 'validate': True}
                else:
                    log.warning(f'login failure, wanted: {user._user_id}, found: {user_id}')
                    return {'ok': False, 'error': 'Lgin failed'}
            else:
                activate = (UsersCollection().records() == 0 and 
                    session['address'] == '127.0.0.1') or world.conf.authentication == 'autoenroll'
                session['activated'] = activate
                await save_session(self._sid, session)
                log.success(f'Validated new user [{host_id}] active={activate}')
                UsersTable().from_doc(Doc({
                    'user_id': user_id,
                    'active': activate,
                    'code': None if activate else self.generate_auth_code(),
                    'tries': 0,
                }, oid=host_id)).append()
                self.activate_session(user._user_id, auth, session)
                return {'ok': True, 'validate': not activate}

        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}

    async def hello(self, auth, get_session, save_session):
        session = await get_session(self._sid)
        try:
            text = f'-----BEGIN RSA PUBLIC KEY-----\n{auth["pubKey"]}\n-----END RSA PUBLIC KEY-----'
            session['pubkey'] = RSA.importKey(text)
            session['host_id'] = auth['hostId']
            await save_session(self._sid, session)
            log.warning(f'HELLO PROTOCOL: sid={self._sid} addr={session["address"]} hostId={auth["hostId"]}')
            cipher = PKCS1_OAEP.new(session['pubkey'], SHA256)
            return {
                'ok': True,
                'pubKey': b"".join(self._keyPair.public_key().export_key().split(b'\n')[1:-1]),
                'pemKey': self._keyPair.public_key().export_key(),
                'secret': b64encode(cipher.encrypt('THESECRET'.encode('ascii'))).decode('ascii'),
            }
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}