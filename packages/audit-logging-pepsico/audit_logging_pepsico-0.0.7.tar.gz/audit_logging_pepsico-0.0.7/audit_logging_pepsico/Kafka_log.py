from audit_logging_pepsico.audit import Audit
import audit_logging_pepsico.constants as con
import uuid
from datetime import datetime
from audit_logging_pepsico.kafka_utilities import kafka_produce_events
import json

class KafkaAuditLog:
    def produce_log(self, logger, ip_address=None, channelId=None, systemId=None, customerId=None,
                    userId=None, url=None, operationName=None, orderId=None, coRelationId=None,
                    sourceOrderNumber=None, externalId=None, requestHeader=None, responseCode=None, documentType=None,
                    componentName=None, methodName=None, requestInput=None, responseOutput=None, gpid=None, route=None,
                    kafka_producer=None, kafka_topic=None):
        try:
            ip_addr = ip_address
            id = con.AUDIT_PRIFIX + con.ID_DELIMITER + str(uuid.uuid4())
            createdDate = str(datetime.now())
            interfaceName = con.INTERFACE_NAME
            log_type = con.AUDIT_SERVICE
            audit_obj = Audit(id, channelId, systemId, ip_addr,
                              userId, customerId, createdDate, url, interfaceName, operationName, orderId,
                              coRelationId, sourceOrderNumber,
                              externalId, requestHeader, responseCode, log_type, documentType, componentName,
                              methodName, requestInput, responseOutput, gpid, route)
            logs = audit_obj.__dict__
            produce_events_status, produce_events_status_msg = kafka_produce_events(json.dumps(logs), kafka_producer,
                                                                                    kafka_topic, logger)
            if produce_events_status:
                logger.info("Kafka Audit logs produced successfully")
            return produce_events_status, produce_events_status_msg
        except Exception as err:
            logger.error("----------ERROR----------")
            logger.error(str(err))
            return False, "Exception: " + str(err)
