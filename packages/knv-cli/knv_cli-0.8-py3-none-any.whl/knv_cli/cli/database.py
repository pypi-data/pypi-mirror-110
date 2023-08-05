from os import remove
from os.path import basename, join
from zipfile import ZipFile

from ..processors.gateways.paypal import Paypal
from ..processors.gateways.volksbank import Volksbank
from ..processors.knv.infos import InfoProcessor
from ..processors.knv.revenues.pcbis import PcBisInvoiceProcessor
from ..processors.knv.revenues.shopkonfigurator import ShopkonfiguratorInvoiceProcessor
from ..processors.knv.expenses.bwd import BwdInvoiceProcessor
from ..processors.knv.expenses.edv import EdvInvoiceProcessor
from ..processors.knv.expenses.sammel import SammelInvoiceProcessor
from ..processors.knv.orders import OrderProcessor
from ..processors.knv.shopkonfigurator import ShopkonfiguratorProcessor
from ..structures.invoices.invoices import Invoices
from ..structures.orders.orders import Orders
from ..structures.payments.paypal import PaypalPayments
from ..structures.payments.volksbank import VolksbankPayments
from ..utils import load_json, dump_json
from ..utils import build_path, dedupe, group_data, sort_data, timestamp
from .session import Session


class Database:
    # PROPS

    invoice_processors = {
        'shopkonfigurator': ShopkonfiguratorInvoiceProcessor,
        'pcbis': PcBisInvoiceProcessor,
        'bwd': BwdInvoiceProcessor,
        'edv': EdvInvoiceProcessor,
        'sammel': SammelInvoiceProcessor,
    }

    payment_processors = {
        'paypal': Paypal,
        'volksbank': Volksbank,
    }

    payment_structures = {
        'paypal': PaypalPayments,
        'volksbank': VolksbankPayments,
    }


    def __init__(self, config: dict) -> None:
        # Database files
        self.order_files = build_path(config.order_dir)
        self.info_files = build_path(config.info_dir)

        # Invoice files
        self.invoice_files = {}
        for processor in self.invoice_processors.keys():
            self.invoice_files[processor] = {
                'pdf': build_path(join(config.invoice_dir, processor, 'pdf'), '*.pdf'),
                'data': build_path(join(config.invoice_dir, processor, 'data')),
            }

        # Payment files
        self.payment_files = {}
        for identifier in self.payment_processors.keys():
            self.payment_files[identifier] = build_path(join(config.payment_dir, identifier))

        # Session files
        self.session_files = {
            'sessions': build_path(join(config.session_dir)),
            'invoices': build_path(join(config.session_dir, 'invoices')),
        }

        for identifier in self.payment_processors.keys():
            self.session_files[identifier] = build_path(join(config.session_dir, identifier))


        # Define path to session files
        self.sessions_dir = join(config.data_dir, 'sessions')

        # Define merged data files
        self.db_files = build_path(config.database_dir)

        # Import config
        self.config = config


    # GENERAL methods

    def flush(self) -> None:
        files = self.order_files + self.info_files

        for processor in self.invoice_processors.keys():
            files += self.invoice_files[processor]['data']

        for processor in self.payment_processors.keys():
            files += self.payment_files[processor]

        for file in files:
            remove(file)


    # REBUILD methods

    def rebuild_data(self):
        # Initialize handler
        handler = ShopkonfiguratorProcessor()

        # Load data files for infos & orders
        handler.load_files(self.info_files, 'infos', True)
        handler.load_files(self.order_files, 'orders', True)

        for code, data in group_data(handler.process().data).items():
            dump_json(sort_data(data), join(self.config.database_dir, '{}.json'.format(code)))


    def rebuild_infos(self) -> None:
        # Initialize handler
        handler = InfoProcessor()

        # Select info files to be imported
        import_files = build_path(self.config.import_dir, handler.regex)

        # Extract information from import files
        handler.load_files(import_files).process()

        # Split infos per-month & export them
        for code, data in group_data(handler.data).items():
            dump_json(sort_data(data), join(self.config.info_dir, '{}.json'.format(code)))


    def rebuild_invoices(self) -> None:
        for identifier, invoice_processor in self.invoice_processors.items():
            # Initialize handler
            handler = invoice_processor()

            # Select invoice files to be imported
            import_files = build_path(self.config.import_dir, handler.regex)

            # Set directory for extracted invoice files
            invoice_dir = join(self.config.invoice_dir, identifier)

            # Extract invoices from archives
            for file in import_files:
                with ZipFile(file) as archive:
                    for zipped_invoice in archive.namelist():
                        archive.extract(zipped_invoice, join(invoice_dir, 'pdf'))

            # .. and extract information from them
            handler.load_files(build_path(join(self.config.invoice_dir, identifier, 'pdf'), '*.pdf')).process()

            # Split invoice data per-month & export it
            for code, data in group_data(handler.data).items():
                dump_json(sort_data(data), join(invoice_dir, 'data', '{}.json'.format(code)))


    def rebuild_orders(self) -> None:
        # Initialize handler
        handler = OrderProcessor()

        # Select order files to be imported
        import_files = build_path(self.config.import_dir, handler.regex)

        # Extract information from import files
        handler.load_files(import_files).process()

        # Split orders per-month & export them
        for code, data in group_data(handler.data).items():
            dump_json(sort_data(data), join(self.config.order_dir, '{}.json'.format(code)))


    def rebuild_payments(self) -> None:
        for identifier, gateway in self.payment_processors.items():
            # Initialize payment gateway handler
            handler = gateway()

            # Apply VKN & blocklist CLI options
            handler.VKN = self.config.vkn
            handler.blocklist = self.config.blocklist

            # Select payment files to be imported
            import_files = build_path(self.config.import_dir, handler.regex)

            # Extract information from import files
            handler.load_files(import_files).process()

            # Split payments per-month & export them
            for code, data in group_data(handler.data).items():
                dump_json(sort_data(data), join(self.config.payment_dir, identifier, '{}.json'.format(code)))


    # GET methods

    def get_invoices(self, invoice_files: list = None) -> Invoices:
        # Select appropriate source files (if available), otherwise ..
        if not invoice_files:
            # .. select all invoice files
            invoice_files = []

            for processor in self.invoice_processors.keys():
                invoice_files += self.invoice_files[processor]['data']

        invoices = load_json(invoice_files)

        # Update invoices with session data
        invoices.update(load_json(self.session_files['invoices']))

        return Invoices(invoices)


    def get_orders(self, order_files: list = None):
        # Select appropriate source files
        order_files = order_files if order_files else self.db_files
        invoice_files = self.invoice_files['shopkonfigurator']['data'] + self.invoice_files['pcbis']['data']

        return Orders(load_json(order_files), load_json(invoice_files))


    def get_payments(self, identifier: str, payment_files: list = None):
        # Select & load appropriate source files
        payment_files = payment_files if payment_files else self.payment_files[identifier]
        payments = load_json(payment_files)

        # Update payments with session data
        payments.update(load_json(self.session_files[identifier]))

        # Select all invoice files
        invoice_files = []

        for processor in self.invoice_processors.keys():
            invoice_files += self.invoice_files[processor]['data']

        return self.payment_structures[identifier](payments, load_json(self.db_files), load_json(invoice_files))


    def get_data(self, identifier: str) -> dict:
        data = load_json(self.db_files)

        return {} if identifier not in data else data[identifier]


    def get_info(self, identifier: str) -> dict:
        infos = load_json(self.info_files)

        return {} if identifier not in infos else infos[identifier]


    def get_invoice(self, identifier: str) -> dict:
        invoices = {}

        # Fetch invoices from database
        for processor in self.invoice_processors.keys():
            invoices.update(load_json(self.invoice_files[processor]['data']))

        # Update invoices with session data
        invoices.update(load_json(self.session_files['invoices']))

        return {} if identifier not in invoices else invoices[identifier]


    def get_order(self, identifier: str) -> dict:
        orders = load_json(self.order_files)

        return {} if identifier not in orders else orders[identifier]


    def get_payment(self, identifier: str) -> dict:
        payments = {}

        # Fetch payments from database
        for processor in self.payment_processors.keys():
            payments.update(load_json(self.payment_files[processor]))

        # Update payments with session data
        payments.update(load_json(self.session_files['paypal']))

        return {} if identifier not in payments else payments[identifier]


    # ACCOUNTING methods

    def has_session(self) -> bool:
        return len(self.session_files['sessions']) > 0


    def import_session(self) -> None:
        for identifier in self.session_files.keys():
            # Skip session files
            if identifier == 'sessions': continue

            # Combine session data, where previous sessions are replaced with current one
            # (1) Load data of previous sessions
            session_data = load_json(self.session_files[identifier])

            # (2) Merge data with current session
            session_data.update(load_json(build_path(self.sessions_dir, '{}_*.json'.format(identifier))))

            # (3) Write changes to disk
            for code, data in group_data(session_data).items():
                dump_json(sort_data(data), join(self.sessions_dir, identifier, '{}.json'.format(code)))


    def load_session(self) -> Session:
        session_files = {}

        for session_file in build_path(self.sessions_dir):
            identifier = basename(session_file).split('_')[0]

            if identifier not in session_files:
                session_files[identifier] = []

            session_files[identifier].append(session_file)

        return Session(session_files)


    def reset_session(self) -> None:
        for file in self.session_files['sessions']:
            remove(file)


    def save_session(self, data: list, identifier: str) -> None:
        # Convert data
        data = {item.identifier(): item.export() for item in data}

        # Save results
        dump_json(data, join(self.sessions_dir, '{identifier}_{timestamp}.json'.format(identifier=identifier, timestamp=timestamp())))
