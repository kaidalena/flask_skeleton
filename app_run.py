import sys

from app import logger, flask_app
from app.database.connection import init_db_conf
from app.tools.log_message_halper import log_msg
from app.tools.script_params import create_parser

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])
configuration = namespace.configuration


try:
    init_db_conf(configuration)

    logger.info(
        log_msg(
            msg='---------- start app ----------',
            source='__init__'
        )
    )

    # на linux необходимо закоментировать
    flask_app.run()
except Exception as ex:
    logger.error(log_msg(
        msg='ERROR in the initialization of the application',
        source='__init__'
    ))