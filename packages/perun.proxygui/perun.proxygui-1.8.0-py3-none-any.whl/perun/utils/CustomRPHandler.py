from cryptojwt import as_unicode
from idpyoidc import verified_claim_name
from idpyoidc.client.oidc import RP
from idpyoidc.client.rp_handler import RPHandler, logger
from idpyoidc.exception import MessageException, NotForMe, MissingRequiredAttribute
from idpyoidc.message.oidc.session import BackChannelLogoutRequest

"""
Custom class overriding RPHandler from idpy-oidc library. It's used solely
in the backchannel logout endpoint for decoding JWT token and performing OIDC
checks on the logout information inside the JWT.
"""


class CustomRPHandler(RPHandler):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def backchannel_logout(self, client: RP, request="", request_args=None) -> str:
        """
        Custom method for backchannel logout. It supports backchannel logout
        only with 'sub' information. Stock idpy-oidc backchannel_logout method
        returns a state whereas we're looking only for the 'sub' attribute from
        the validated JWT token.

        :param client: OIDC client implementation
        :param request: URL encoded logout request
        :param request_args: arguments from the URL encoded logout request
        :return: sub - OIDC subject id from validated JWT
        """
        if request_args:
            req = BackChannelLogoutRequest(**request_args)
        elif request:
            req = BackChannelLogoutRequest().from_urlencoded(as_unicode(request))
        else:
            raise MissingRequiredAttribute("logout_token")

        _context = client.get_context()

        kwargs = {
            "aud": client.client_id,
            "iss": _context.get("issuer"),
            "keyjar": client.get_attribute("keyjar"),
            "allowed_sign_alg": _context.get("registration_response").get(
                "id_token_signed_response_alg", "RS256"
            ),
        }

        logger.debug(f"(backchannel_logout) Verifying request using: {kwargs}")
        try:
            req.verify(**kwargs)
        except (MessageException, ValueError, NotForMe) as err:
            raise MessageException("Bogus logout request: {}".format(err))
        else:
            logger.debug("Request verified OK")

        # We're looking only for sub as sid logout is not supported in our
        # implementation
        sub = req[verified_claim_name("logout_token")].get("sub")

        if not sub:
            raise MessageException(
                "This endpoint supports backchannel logout for all user's "
                "sessions using only sub and it was not provided in the "
                "logout request."
            )

        return sub
