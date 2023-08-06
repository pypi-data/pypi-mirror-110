from datetime import timezone

from .address import Address
from .simpletypes import Balance
from . import exceptions


class WalletService(object):
    """
    Represents the service responsible for listing and retrieving the existing wallets or creating
    new ones.

    :param backend: the backend used to handle the underlying service layer

    """

    def __init__(self, backend=None):
        self.backend = backend

    def wallets(self):
        return [Wallet(wid, backend=self.backend) for wid in self.backend.wallet_ids()]

    def wallet(self, wid, passphrase=None):
        return Wallet(wid, backend=self.backend, passphrase=passphrase)

    def create_wallet(self, name, mnemonic, passphrase, mnemonic_2f=None):
        """
        Creates/restores a wallet. Returns only ID as the backend may need some time to sync
        before being able to return full wallet data.
        """
        return self.backend.create_wallet(name, mnemonic, passphrase, mnemonic_2f)


class Wallet(object):
    """
    Represents a single wallet. Allows for browsing the history, checking balance and spending
    funds.

    :param wid:         the wallet ID
    :param backend:     the backend used to handle the underlying service layer
    :param passphrase:  the passphrase protecting the wallet's spending functionality, not required
                        for read-only operations. It will be stored for the entire lifetime of the
                        object in ``.passphrase`` field. It might be also provided for each
                        individual spend operation, then it will be discarded after use.
    """

    passphrase = None

    def __init__(self, wid, backend, passphrase=None):
        self.wid = wid
        self.backend = backend
        self.passphrase = passphrase or self.passphrase
        if not self.backend.wallet_exists(wid):
            raise ValueError("Wallet of id '{:s}' doesn't exist.".format(wid))

    def sync_progress(self):
        return self.backend.sync_progress(self.wid)

    def addresses(self, with_usage=False):
        if with_usage:
            return [
                (Address(addr[0], wallet=self), addr[1])
                for addr in self.backend.addresses(self.wid)
            ]
        return [
            Address(addr[0], wallet=self) for addr in self.backend.addresses(self.wid)
        ]

    def balance(self):
        return self.backend.balance(self.wid)

    def assets(self):
        return self.backend.asset_balances(self.wid)

    def delete(self):
        return self.backend.delete_wallet(self.wid)

    def transactions(self):  # , start=None, end=None, order="ascending"):
        # WARNING: parameters don't really work; this is a known bug
        # if start:
        #    start = start.astimezone(tz=timezone.utc)
        # if end:
        #    end = end.astimezone(tz=timezone.utc)
        return self.backend.transactions(
            self.wid
        )  # , start=start, end=end, order=order)

    def _resolve_passphrase(self, passphrase):
        passphrase = passphrase or self.passphrase
        if passphrase is None:
            raise exceptions.MissingPassphrase(
                "Cannot perform operation without the passphrase"
            )
        return passphrase

    def transfer(self, address, amount, metadata=None, ttl=None, passphrase=None):
        """
        Sends a transfer from the wallet. Returns the resulting transaction.

        :param address: destination :class:`Address <cardano.address.Address>` or subtype
        :param amount: amount to send
        :param metadata: metadata to be sent, as :class:`Metadata <cardano.metadata.Metadata>`
                    instance od ``dict`` mapping ``int`` keys to values of acceptable types
        :param ttl: Time To Live in seconds. After TTL has lapsed the nodes give up on broadcasting
                    the transaction. Leave `None` to use the default value.
        :param passphrase: the passphrase to the wallet. It takes precedence over `self.passphrase`
                    and is discarded after use. If neither `self.passphrase` nor `passphrase` is
                    set, a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                    exception will be raised.
        :rtype: :class:`Transaction <cardano.transaction.Transaction>`
        """
        return self.backend.transfer(
            self.wid,
            ((address, amount),),
            metadata=metadata,
            ttl=ttl,
            passphrase=self._resolve_passphrase(passphrase),
        )

    def transfer_multiple(
        self, destinations, amount, metadata=None, ttl=None, passphrase=None
    ):
        """
        Sends multiple transfers from the wallet. Returns the resulting transaction.

        :param destinations: a list of :class:`Address <cardano.address.Address>` and amount
                    pairs ``[(address, amount), ...]``
        :param metadata: metadata to be sent, as :class:`Metadata <cardano.metadata.Metadata>`
                    instance od ``dict`` mapping ``int`` keys to values of acceptable types
        :param ttl: Time To Live in seconds. After TTL has lapsed the nodes give up on broadcasting
                    the transaction. Leave `None` to use the default value.
        :param passphrase: the passphrase to the wallet. It takes precedence over `self.passphrase`
                    and is discarded after use. If neither `self.passphrase` nor `passphrase` is
                    set, a :class:`MissingPassphrase <cardano.exceptions.MissingPassphrase>`
                    exception will be raised.
        :rtype: :class:`Transaction <cardano.transaction.Transaction>`
        """
        passphrase = passphrase or self.passphrase
        if passphrase is None:
            raise exceptions.MissingPassphrase(
                "Cannot transfer from wallet without the passphrase"
            )
        return self.backend.transfer(
            self.wid,
            destinations,
            metadata=metadata,
            ttl=ttl,
            passphrase=self._resolve_passphrase(passphrase),
        )
