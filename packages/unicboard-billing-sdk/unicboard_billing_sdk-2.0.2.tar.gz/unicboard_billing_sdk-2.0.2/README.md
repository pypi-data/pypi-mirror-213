# [BILLING API DOCUMENTATION](https://uniclab-01.github.io/billing-api)


# Unicboard public api (in developing):


## base station api

### get base station type api list

method: GET<br/> 
route: '/base-stations/types'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "name": str
    "notes": str
]
```

### get base station type api object
method: GET<br/> 
route: '/base-stations/types/<base_station_type_id>'<br/>
request:<br/>
```json
    "base_station_type_id": UUID
```
response:
```json
    "id": UUID
    "name": str
    "notes": str
```

### create base station type api
method: POST<br/> 
route: '/base-stations/types'<br/>
request:<br/>
body:<br/>
```json
    "name": str
    "notes": str
```
response:
```json
    "id": UUID
    "name": str
    "notes": str
```

### modification base station type api
method: PUT<br/> 
route: '/base-stations/types/<base_station_type_id>'<br/>
request:<br/>
```json
    "base_station_type_id": UUID
```
body:<br/>
```json
    "name": str
    "notes": str
```
response:
```json
    "id": UUID
    "name": str
    "notes": str
```

### get base station api list

method: GET<br/> 
route: '/base-stations'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "identifier": str
    "base_station_type": {
        "id": UUID
        "name": str
        "notes": str
    }
]
```

### get base station api object

method: GET<br/> 
route: '/base-stations/<base_station_id>'<br/>
request:<br/>
```json
  "base_station_id": UUID
```
response:
```json
    "id": UUID
    "identifier": str
    "base_station_type": {
        "id": UUID
        "name": str
        "notes": str
    }
```

### create base station api

method: POST<br/> 
route: '/base-stations'<br/>
request:<br/>
body:<br/>
```json
    "base_station_type_id": UUID
    "identifier": str
```
response:
```json
    "id": UUID
    "identifier": str
    "base_station_type": {
        "id": UUID
        "name": str
        "notes": str
    }
```

### modification base station api

method: PUT<br/> 
route: '/base-stations/<base_station_id>'<br/>
request:<br/>
```json
    "base_station_id": UUID
```
body:<br/>
```json
    "base_station_type_id": UUID
    "identifier": str
```
response:
```json
    "id": UUID
    "identifier": str
    "base_station_type": {
        "id": UUID
        "name": str
        "notes": str
    }
```


## network api

### get network api list

method: GET<br/> 
route: '/networks'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "name": str
    "type_network": str
    "data_gateway_id": UUID4
    "sys_type": str
    "specifier": Optional[str]
    "params": Optional[Dict[str, Any]]
]
```

### get network api object

method: GET<br/> 
route: '/networks/<network_id>'<br/>
request:<br/>
```json
    "network_id": UUID
```
response:
```json
    "id": UUID
    "name": str
    "type_network": str
    "data_gateway_id": UUID4
    "sys_type": str
    "specifier": Optional[str]
    "params": Optional[Dict[str, Any]]
```

### create network api

method: POST<br/> 
route: '/networks'<br/>
request:<br/>
body:<br/>
```json
    "name": str
    "type_network": str (input/output)
    "sys_type": str (INPUT_NBIOT/INPUT_LORA/OUTPUT_DATA_LOGGER_DEVICE_DATA/OUTPUT_DATA_AGGREGATOR_DEVICE_DATA)
    "specifier": Optional[str]
```
response:
```json
    "id": UUID
    "name": str
    "type_network": str
    "data_gateway_id": UUID4
    "sys_type": str
    "specifier": Optional[str]
    "params": Optional[Dict[str, Any]]
```

### modification network api

method: PUT<br/> 
route: '/networks/<network_id>'<br/>
request:<br/>
```json
    "network_id": UUID
```
body:<br/>
```json
    "name": str
    "type_network": str (input/output)
    "sys_type": str (INPUT_NBIOT/INPUT_LORA/OUTPUT_DATA_LOGGER_DEVICE_DATA/OUTPUT_DATA_AGGREGATOR_DEVICE_DATA)
    "specifier": Optional[str]
```
response:
```json
    "id": UUID
    "name": str
    "type_network": str
    "data_gateway_id": UUID4
    "sys_type": str
    "specifier": Optional[str]
    "params": Optional[Dict[str, Any]]
```


## device api

### get device api list

method: GET<br/> 
route: '/devices'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "manufacturer_serial_number": str
    "firmware_version": Optional[str]
    "hardware_version": Optional[str]
    "date_produced": Optional[datetime]
    "hacks": List[str]
    "device_tz": Optional[str]
    "device_clock_offset_s": Optional[int]
    "time_transition": str
    "device_manufacturer": {
      "id": UUID4,
      "name": str
    },
    "device_modification": {
        "id": UUID4,
        "name": Optional[str],
        "device_modification_type_id": Optional[UUID4],
        "device_modification_type": {
            "id": UUID4,
            "sys_name": str,
            "name_ru": str,
            "name_en": str,
            "type": str,
            "metering_type_id": UUID4,
            "device_metering_type": {
                "id": UUID4,
                "sys_name": str,
                "name_ru": str,
                "name_en": str
            }
        }
    
    }
    "device_channel": [
        {
            "device_id": UUID4
            "serial_number": int
            "last_date_event_no_data": Optional[datetime]
            "inactivity_limit": Optional[int]
            "device_meter": [
                {
                    "device_channel_id": UUID
                    "value_multiplier": Optional[float]
                    "unit_multiplier": Optional[float]
                    "kind": str
                }
            ]
        }
    ]
    "data_gateway_network_device": Optional[
    {
        "id": UUID4
        "uplink_protocol_id": UUID4
        "downlink_protocol_id": UUID4
        "data_gateway_network_id": UUID4
        "mac": int
        "key_id": Optional[UUID4]
        "device_id": UUID4
        "uplink_encryption_key": Optional[str]
        "downlink_encryption_key": Optional[str]
        "encryption_key": Optional[str]
        "protocol":
        {
            "id": UUID4
            "date_created": datetime
            "date_modified": datetime
            "name": str
            "type": ProtocolEnum
        }
        "network": Optional[
        {
            "id": UUID
            "name": str
            "type_network": str
            "data_gateway_id": UUID4
            "sys_type": str
            "specifier": Optional[str]
            "params": Optional[Dict[str, Any]]
        }]
    }]
]
```

### get device api object

method: GET<br/> 
route: '/devices/<device_id>'<br/>
request:<br/>
```json
    "device_id": UUID
```
response:
```json
"manufacturer_serial_number": str
"firmware_version": Optional[str]
"hardware_version": Optional[str]
"date_produced": Optional[datetime]
"hacks": List[str]
"device_tz": Optional[str]
"device_clock_offset_s": Optional[int]
"time_transition": str
"device_manufacturer": {
  "id": UUID4,
  "name": str
},
"device_modification": {
    "id": UUID4,
    "name": Optional[str],
    "device_modification_type_id": Optional[UUID4],
    "device_modification_type": {
        "id": UUID4,
        "sys_name": str,
        "name_ru": str,
        "name_en": str,
        "type": str,
        "metering_type_id": UUID4,
        "device_metering_type": {
            "id": UUID4,
            "sys_name": str,
            "name_ru": str,
            "name_en": str
        }
    }

}
"device_channel": [
    {
        "device_id": UUID4
        "serial_number": int
        "last_date_event_no_data": Optional[datetime]
        "inactivity_limit": Optional[int]
        "device_meter": [
            {
                "device_channel_id": UUID
                "value_multiplier": Optional[float]
                "unit_multiplier": Optional[float]
                "kind": str
            }
        ]
    }
]
"data_gateway_network_device": Optional[
{
    "id": UUID4
    "uplink_protocol_id": UUID4
    "downlink_protocol_id": UUID4
    "data_gateway_network_id": UUID4
    "mac": int
    "key_id": Optional[UUID4]
    "device_id": UUID4
    "uplink_encryption_key": Optional[str]
    "downlink_encryption_key": Optional[str]
    "encryption_key": Optional[str]
    "protocol":
    {
        "id": UUID4
        "date_created": datetime
        "date_modified": datetime
        "name": str
        "type": ProtocolEnum
    }
    "network": Optional[
    {
        "id": UUID
        "name": str
        "type_network": str
        "data_gateway_id": UUID4
        "sys_type": str
        "specifier": Optional[str]
        "params": Optional[Dict[str, Any]]
    }]
}]
```

### crate device api

method: POST<br/> 
route: '/devices/'<br/>
request:<br/>
body:<br/>
```json
    "manufacturer_name": str
    "mac": int
    "manufacturer_serial_number": str
    "modification_type_id": UUID4
    "modification_id": UUID4
    "date_produced": Optional[datetime]
    "firmware_version": Optional[str]
    "hardware_version": Optional[str]
    "uplink_protocol_id": UUID4
    "downlink_protocol_id": UUID4
    "uplink_encryption_type": str (NO_ENCRYPTION/XTEA_V_NERO_V0/AES_ECB_V_NERO_V0/KUZNECHIK_V_NERO_V0)
    "downlink_encryption_type": str (NO_ENCRYPTION/XTEA_V_NERO_V0/AES_ECB_V_NERO_V0/KUZNECHIK_V_NERO_V0)
    "key_id": Optional[UUID4]
    "uplink_encryption_key": Optional[str]
    "downlink_encryption_key": Optional[str]
    "data_input_gateway_network_id": UUID4
    "data_gateway_id": UUID4
    "device_channels": List[
      {
          "serial_number": int
          "inactivity_limit": Optional[int]
          "device_meter": List[
            {
                "value_multiplier": float
                "unit_multiplier": float
                "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
            }
          ]        
      }
    ]
    "modification_name": Optional[str]
    "modification_type_name": Optional[str]
```
response:<br/>
```json
    "manufacturer_serial_number": str
    "firmware_version": Optional[str]
    "hardware_version": Optional[str]
    "date_produced": Optional[datetime]
    "device_manufacturer": {
        "id": UUID
        "name": str
    }
    "device_modification": {
        "id": UUID
        "name": Optional[str]
        "device_modification_type_id": Optional[UUID]
        "device_modification_type": {
            "id": UUID
            "sys_name": str
            "name_ru": str
            "name_en": str
            "type": str (smart_meter/modem)
            "metering_type_id": UUID
            "device_metering_type": {
                "id": UUID
                "sys_name": str
                "name_ru": str
                "name_en": str
            }
        }
    }
    "device_channel": [
    {
        "serial_number": int
        "inactivity_limit": Optional[int]
        "device_meter": [
            {
                "device_channel_id": UUID
                "value_multiplier": Optional[float]
                "unit_multiplier": Optional[float]
                "kind": str
            }
        ]
    }
    ]
    "data_gateway_network_device": Optional[
    {
        "id": UUID4
        "uplink_protocol_id": UUID4
        "downlink_protocol_id": UUID4
        "data_gateway_network_id": UUID4
        "mac": int
        "key_id": Optional[UUID4]
        "device_id": UUID4
        "uplink_encryption_key": Optional[str]
        "downlink_encryption_key": Optional[str]
        "encryption_key": Optional[str]
        "protocol":
        {
            "id": UUID4
            "date_created": datetime
            "date_modified": datetime
            "name": str
            "type": ProtocolEnum
        }
        "network": Optional[
        {
            "id": UUID
            "name": str
            "type_network": str
            "data_gateway_id": UUID4
            "sys_type": str
            "specifier": Optional[str]
            "params": Optional[Dict[str, Any]]
        }]
    }]
```

### modification device api

method: PUT<br/> 
route: '/devices/<device_id>'<br/>
request:<br/>
```json
    "device_id": UUID
```
body:<br/>
```json
    "device_modification_id": UUID
    "device_manufacturer_id": UUID
    "manufacturer_serial_number": str
    "date_produced": DateTime
    "firmware_version": str
    "hardware_version": str
    "device_tz": str
    "device_clock_offset_s": int
    "time_transition": str (summer/winter/unknown)
```
response:<br/>
```json
    "device_id": UUID
    "device_modification_id": UUID
    "device_manufacturer_id": UUID
    "manufacturer_serial_number": str
    "date_produced": DateTime
    "firmware_version": str
    "hardware_version": str
    "device_tz": str
    "device_clock_offset_s": int
    "time_transition": str (summer/winter/unknown)
```

### delete device api

method: DELETE<br/> 
route: '/devices/<device_id>'<br/>
request:<br/>
```json
    "device_id": UUID
```
response:<br/> 200


## device network api

### get device network api list

method: GET<br/> 
route: '/devices-networks/'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID4
    "uplink_protocol_id": UUID4
    "downlink_protocol_id": UUID4
    "data_gateway_network_id": UUID4
    "mac": int
    "key_id": Optional[UUID4]
    "device_id": UUID4
    "uplink_encryption_key": Optional[str]
    "downlink_encryption_key": Optional[str]
    "device": {
        "manufacturer_serial_number": str
        "firmware_version": Optional[str]
        "hardware_version": Optional[str]
        "date_produced": Optional[datetime]
        "device_manufacturer": {
            "id": UUID4
            "name": str
        }
        "device_modification": {
            "id": UUID4
            "name": Optional[str]
            "device_modification_type_id": Optional[UUID4]
            "device_modification_type": {
                "id": UUID4
                "sys_name": str
                "name_ru": str
                "name_en": str
                "type": str (smart_meter/modem)
                "metering_type_id": UUID4
                "device_metering_type": {
                    "id": UUID4
                    "sys_name": str
                    "name_ru": str
                    "name_en": str
                }     
            }
        }
        "device_channel": List[{
            "serial_number": int
            "inactivity_limit": Optional[int]
            "device_meter": [
                {
                    "device_channel_id": UUID
                    "value_multiplier": Optional[float]
                    "unit_multiplier": Optional[float]
                    "kind": str
                }
            ]
        }]
    }
    "network": {
        "id": UUID
        "uplink_protocol_id": UUID
        "downlink_protocol_id": UUID
        "data_gateway_network_id": UUID
        "mac": int
        "key_id": Optional[UUID]
        "device_id": UUID
        "uplink_encryption_key": Optional[str]
        "downlink_encryption_key": Optional[str]
        "encryption_key": Optional[str]
        "protocol": {
            id: UUID
            name: str
            type: str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0)
        }
        "network": Optional[
            "name": str
            "type_network": str(input/output)
            "data_gateway_id": UUID
            "data_gateway": {
              "name": str
            } 
            "sys_type": str (INPUT_NBIOT/INPUT_LORA/OUTPUT_DATA_LOGGER_DEVICE_DATA/OUTPUT_DATA_AGGREGATOR_DEVICE_DATA)
            "specifier": Optional[str]
            "params": Optional[Dict[str, Any]]
      ]
  }
]
```

### get device network api object

method: GET<br/> 
route: '/devices-networks/<device_network_id>'<br/>
request:<br/>
```json
    "device_network_id": UUID
```
response:
```json
"id": UUID4
"uplink_protocol_id": UUID4
"downlink_protocol_id": UUID4
"data_gateway_network_id": UUID4
"mac": int
"key_id": Optional[UUID4]
"device_id": UUID4
"uplink_encryption_key": Optional[str]
"downlink_encryption_key": Optional[str]
"device": {
    "manufacturer_serial_number": str
    "firmware_version": Optional[str]
    "hardware_version": Optional[str]
    "date_produced": Optional[datetime]
    "device_manufacturer": {
        "id": UUID4
        "name": str
    }
    "device_modification": {
        "id": UUID4
        "name": Optional[str]
        "device_modification_type_id": Optional[UUID4]
        "device_modification_type": {
            "id": UUID4
            "sys_name": str
            "name_ru": str
            "name_en": str
            "type": str (smart_meter/modem)
            "metering_type_id": UUID4
            "device_metering_type": {
                "id": UUID4
                "sys_name": str
                "name_ru": str
                "name_en": str
            }     
        }
    }
    "device_channel": List[{
        "serial_number": int
        "inactivity_limit": Optional[int]
        "device_meter": [
            {
                "device_channel_id": UUID
                "value_multiplier": Optional[float]
                "unit_multiplier": Optional[float]
                "kind": str
            }
        ]
    }]
}
"network": {
    "id": UUID
    "uplink_protocol_id": UUID
    "downlink_protocol_id": UUID
    "data_gateway_network_id": UUID
    "mac": int
    "key_id": Optional[UUID]
    "device_id": UUID
    "uplink_encryption_key": Optional[str]
    "downlink_encryption_key": Optional[str]
    "encryption_key": Optional[str]
    "protocol": {
        id: UUID
        name: str
        type: str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0)
    }
    "network": Optional[
        "name": str
        "type_network": str(input/output)
        "data_gateway_id": UUID
        "data_gateway": {
          "name": str
        } 
        "sys_type": str (INPUT_NBIOT/INPUT_LORA/OUTPUT_DATA_LOGGER_DEVICE_DATA/OUTPUT_DATA_AGGREGATOR_DEVICE_DATA)
        "specifier": Optional[str]
        "params": Optional[Dict[str, Any]]
  ]
}
```

### create device network api

method: POST<br/> 
route: '/devices-networks'<br/>
request:<br/>
body:<br/>
```json
    "mac": int
    "uplink_encryption_key": str
    "downlink_encryption_key": str
    "uplink_encryption_type": str
    "downlink_encryption_type": str
    "key_id": str
    "device_id": UUID
    "data_gateway_network_id": UUID
    "uplink_protocol_id": UUID
    "downlink_protocol_id": UUID
```
response:
```json
    "id": UUID4
    "mac": int
    "uplink_encryption_key": str
    "downlink_encryption_key": str
    "uplink_encryption_type": str
    "downlink_encryption_type": str
    "key_id": str
    "device_id": UUID
    "data_gateway_network_id": UUID
    "uplink_protocol_id": UUID
    "downlink_protocol_id": UUID
```

### modification device network api

method: PUT<br/> 
route: '/devices-networks/<device_network_id>'<br/>
request:<br/>
```json
    "device_network_id": UUID
```
body:<br/>
```json
    "mac": int
    "uplink_encryption_key": str
    "downlink_encryption_key": str
    "uplink_encryption_type": str
    "downlink_encryption_type": str
    "key_id": str
    "device_id": UUID
    "data_gateway_network_id": UUID
    "uplink_protocol_id": UUID
    "downlink_protocol_id": UUID
```
response:
```json
    "id": UUID4
    "mac": int
    "uplink_encryption_key": str
    "downlink_encryption_key": str
    "uplink_encryption_type": str
    "downlink_encryption_type": str
    "key_id": str
    "device_id": UUID
    "data_gateway_network_id": UUID
    "uplink_protocol_id": UUID
    "downlink_protocol_id": UUID
```

### delete device network api

method: DELETE<br/> 
route: '/devices-networks/<device_network_id>'<br/>
request:<br/>
```json
    "device_network_id": UUID
```
response: 200


## device channel api

### get device channel api list

method: GET<br/> 
route: '/channels'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "device_id": UUID4
    "serial_number": int
    "last_date_event_no_data": Optional[datetime]
    "inactivity_limit": Optional[int]
    "device_meter": [
        "device_channel_id": UUID
        "value_multiplier": Optional[float]
        "unit_multiplier": Optional[float]
        "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
    ]
]
```

### get device channel api list by device

method: GET<br/> 
route: '/devices/<device_id>/channels'<br/>
request:<br/>
```json
    "device_id": UUID
```
response:
```json
[
    "device_id": UUID4
    "serial_number": int
    "last_date_event_no_data": Optional[datetime]
    "inactivity_limit": Optional[int]
    "device_meter": [
        "device_channel_id": UUID
        "value_multiplier": Optional[float]
        "unit_multiplier": Optional[float]
        "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
    ]
]
```

### get device channel api object

method: GET<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
```
response:
```json
    "device_id": UUID4
    "serial_number": int
    "last_date_event_no_data": Optional[datetime]
    "inactivity_limit": Optional[int]
    "device_meter": [
        "device_channel_id": UUID
        "value_multiplier": Optional[float]
        "unit_multiplier": Optional[float]
        "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
    ]
```

### create device channel api

method: POST<br/> 
route: '/devices/<device_id>/channels'<br/>
request:<br/>
```json
    "device_id": UUID
```
body:<br/>
```json
    "device_id": UUID
    "serial_number": int
    "inactivity_limit": Optional[int]
```
response:
```json
    "device_id": UUID4
    "serial_number": int
    "last_date_event_no_data": Optional[datetime]
    "inactivity_limit": Optional[int]
    "device_meter": [
        "device_channel_id": UUID
        "value_multiplier": Optional[float]
        "unit_multiplier": Optional[float]
        "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
    ]
```
### modification device channel api

method: PUT<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
```
body:<br/>
```json
    "device_id": UUID
    "serial_number": int
    "inactivity_limit": Optional[int]
```
response:
```json
    "device_id": UUID4
    "serial_number": int
    "last_date_event_no_data": Optional[datetime]
    "inactivity_limit": Optional[int]
    "device_meter": [
        "device_channel_id": UUID
        "value_multiplier": Optional[float]
        "unit_multiplier": Optional[float]
        "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
    ]
```

### delete device channel api

method: DELETE<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
```
response: 200


## device meter api

### get device meter api list

method: GET<br/> 
route: '/meters'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "device_channel_id": UUID
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
]
```

### get device meter api list by channel

method: GET<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>/meters'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
```
response:
```json
[
    "id": UUID
    "device_channel_id": UUID
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
]
```

### get device meter api object

method: GET<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>/meters/<meter_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
    "meter_id": UUID
```
response:
```json
    "id": UUID
    "device_channel_id": UUID
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
```

### create device meter api

method: POST<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>/meters'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
```
body:<br/>
```json
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
```
response:
```json
    "id": UUID
    "device_channel_id": UUID
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
```

### modification device meter api

method: PUT<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>/meters/<meter_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
    "meter_id": UUID
```
body:<br/>
```json
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
```
response:
```json
    "id": UUID
    "device_channel_id": UUID
    "value_multiplier": Optional[float]
    "unit_multiplier": Optional[float]
    "kind": str (COMMON_CONSUMED/COMMON_GENERATED/COMMON_ACTIVE_GENERATED/COMMON_ACTIVE_CONSUMED/COMMON_REACTIVE_GENERATED/COMMON_REACTIVE_CONSUMED/PHASE_A_ACTIVE_CONSUMED/PHASE_A_ACTIVE_GENERATED/PHASE_A_REACTIVE_CONSUMED/PHASE_A_REACTIVE_GENERATED/PHASE_B_ACTIVE_CONSUMED/PHASE_B_ACTIVE_GENERATED/PHASE_B_REACTIVE_CONSUMED/PHASE_B_REACTIVE_GENERATED/PHASE_C_ACTIVE_CONSUMED/PHASE_C_ACTIVE_GENERATED/PHASE_C_REACTIVE_CONSUMED/PHASE_C_REACTIVE_GENERATED)
```


### delete device meter api

method: DELETE<br/> 
route: '/devices/<device_id>/channels/<device_channel_id>/meters/<meter_id>'<br/>
request:<br/>
```json
    "device_id": UUID
    "device_channel_id": UUID
    "meter_id": UUID
```
response: 200


## device manufacturer api

### get device manufacturer api list

method: GET<br/> 
route: '/manufacturers'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "name" : str
]
```

### get device manufacturer api object

method: GET<br/> 
route: '/manufacturers/<manufacturer_id>'<br/>
request:<br/>
```json
    "manufacturer_id": UUID
```
response:
```json
    "id": UUID
    "name" : str
```

### create device manufacturer api object

method: POST<br/>
route: '/manufacturers'<br/>
request:<br/>
body:<br/>
```json
  "name" : str
```
response:
```json
    "id": UUID
    "name" : str
```

### modification device manufacturer api object

method: PUT<br/>
route: '/manufacturers/<manufacturer_id>'<br/>
request:<br/>
```json
  "manufacturer_id" : UUID
```
body:<br/>
```json
  "name" : str
```
response:
```json
    "id": UUID
    "name" : str
```

### delete device manufacturer api object

method: DELETE<br/>
route: '/manufacturers/<manufacturer_id>'<br/>
request:<br/>
```json
  "manufacturer_id" : UUID
```
response: 200


## metering type api

### get metering type api list

method: GET<br/> 
route: '/metering-types'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "sys_name": str
    "name_ru": str
    "name_en": str
]
```

### get metering type api object

method: GET<br/> 
route: '/metering-types/<metering_type_id>'<br/>
request:<br/>
```json
    "metering_type_id": UUID
```
response:
```json
    "id": UUID
    "sys_name": str
    "name_ru": str
    "name_en": str
```

### create metering type api object

method: POST<br/>
route: '/metering-types'<br/>
request:<br/>
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
```
response:
```json
    "id": UUID
    "sys_name": str
    "name_ru": str
    "name_en": str
```

### modification metering type api object

method: PUT<br/>
route: '/metering-types/<metering_type_id>'<br/>
request:<br/>
```json
  "metering_type_id" : UUID
```
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
```
response:
```json
[
    "id": UUID
    "sys_name": str
    "name_ru": str
    "name_en": str
]
```

### delete metering type api object

method: DELETE<br/>
route: '/metering-types/<metering_type_id>'<br/>
request:<br/>
```json
  "metering_type_id" : UUID
```
response: 200


## device modification type api

### get device modification type api list

method: GET<br/> 
route: '/modification-types'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID4
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
    }
]
```

### get device modification type api object

method: GET<br/> 
route: '/modification-types/<modification_type_id>'<br/>
request:<br/>
```json
    "modification_type_id": UUID
```
response:
```json
    "id": UUID4
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
    }
```

### create device modification type api

method: POST<br/> 
route: '/modification-types'<br/>
request:<br/>
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": UUID
```
response:
```json
    "id": UUID4
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
    }
```

### modification device modification type api

method: PUT<br/> 
route: '/modification-types/<modification_type_id>'<br/>
request:<br/>
```json
    "modification_type_id": UUID
```
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": UUID
```
response:
```json
    "id": UUID4
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "device_metering_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
    }
```

### delete device modification type api

method: DELETE<br/> 
route: '/modification-types/<modification_type_id>'<br/>
request:<br/>
```json
    "modification_type_id": UUID
```
response: 200


## device modification api

### get device modification api list

method: GET<br/> 
route: '/modifications'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID4
    "name": str
    "max_daily_consumption": float
    "device_modification_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
        "type": str (smart_meter/modem)
        "device_metering_type": {
            "id": UUID4
            "sys_name": str
            "name_ru": str
            "name_en": str
        }
    }
]
```

### get device modification api object

method: GET<br/> 
route: '/modifications/<modification_id>'<br/>
request:<br/>
```json
    "modification_id": UUID
```
response:
```json
    "id": UUID4
    "name": str
    "max_daily_consumption": float
    "device_modification_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
        "type": str (smart_meter/modem)
        "device_metering_type": {
            "id": UUID4
            "sys_name": str
            "name_ru": str
            "name_en": str
        }
    }
```

### create device modification api

method: POST<br/> 
route: '/modifications'<br/>
request:<br/>
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "metering_type_id": UUID4
```
response:
```json
    "id": UUID4
    "name": str
    "max_daily_consumption": float
    "device_modification_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
        "type": str (smart_meter/modem)
        "device_metering_type": {
            "id": UUID4
            "sys_name": str
            "name_ru": str
            "name_en": str
        }
    }
```

### modofication device modification api

method: PUT<br/> 
route: '/modifications/<modification_id>'<br/>
request:<br/>
```json
    "modification_id": UUID
```
body:<br/>
```json
    "sys_name": str
    "name_ru": str
    "name_en": str
    "type": str (smart_meter/modem)
    "metering_type_id": UUID4
```
response:
```json
    "id": UUID4
    "name": str
    "max_daily_consumption": float
    "device_modification_type": {
        "id": UUID4
        "sys_name": str
        "name_ru": str
        "name_en": str
        "type": str (smart_meter/modem)
        "device_metering_type": {
            "id": UUID4
            "sys_name": str
            "name_ru": str
            "name_en": str
        }
    }
```

### delete device modification api

method: DELETE<br/> 
route: '/modifications/<modification_id>'<br/>
request:<br/>
```json
    "modification_id": UUID
```
response: 200

## protocol api

### get protocol api list

method: GET<br/> 
route: '/protocols'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID4
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
]
```

### get protocol api object

method: GET<br/> 
route: '/protocols/<protocol_id>'<br/>
request:<br/>
```json
    "protocol_id": UUID
```
response:
```json
    "id": UUID4
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
```

### create protocol api

method: POST<br/> 
route: '/protocols'<br/>
request:<br/>
body:<br/>
```json
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
```
response:
```json
    "id": UUID4
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
```

### modification protocol api

method: PUT<br/> 
route: '/protocols/<protocol_id>'<br/>
request:<br/>
```json
    "protocol_id": UUID
```
body:<br/>
```json
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
```
response:
```json
    "id": UUID4
    "name": str
    "type": str (WATER5_V_NERO_V0/NCP_SMP_V0/SMP_V0/SMP_M_GAS_METER_V0/SMP_M_ENERGY_METER_V0/SMP_M_JUPITER_08B_V0/SMP_M_JUPITER_12B_V0/SMP_M_JUPITER_16B_V0/SMP_M_WATER_METER_04B_V0/SMP_M_WATER_METER_08B_V0/SMP_M_WATER_METER_12B_V0/SMP_M_WATER_METER_16B_V0/WATER5_V_JUPITER_FREESCALE_V0/WATER5_V_JUPITER_STM_V0/WATER5_V_FLUO_STM_V0/WATER5_V_FLUO_FREESCALE_V0/WATER5_V_FLUO_A_V0/WATER5_V_FLUO_S_V0/WATER5_V_GAS_V0/WATER5_V_JUPITER_LORA_V0/WATER5_V_FLUO_LORA_V0)
```

### delete protocol api

method: DELETE<br/> 
route: '/protocols/<protocol_id>'<br/>
request:<br/>
```json
    "protocol_id": UUID
```
response: 200


## base station task api

### get base station task api list

method: GET<br/> 
route: '/bs-tasks'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
  "id": UUID
  "effective_macs": List[int],
  "effective_datetime_from": datetime
  "effective_datetime_to": datetime
  "effective_count": int
  "reglament_type": str (schedule,on_capture,immediate)
  "every_s": int
  "reglament_exclusion_time_section": json
  "priority": int
  "regulation": str (immediate, lbt)
  "bs_id": UUID 
  "status": str (created, in_progress, delivered, succeed, failed)
  "task_type": str (time_sync)
  "utc_offeset_s": int
  "protocol":  str (6k7, unbp)
  "time": datetime
]
```

### get base station task api list by base station id

method: GET<br/> 
route: '/bs-tasks/<bs_id>'<br/>
request:<br/>
```json
    "bs_id": UUID
    "limit": int
    "offset": int
```
response:
```json
[
  "id": UUID
  "effective_macs": List[int],
  "effective_datetime_from": datetime
  "effective_datetime_to": datetime
  "effective_count": int
  "reglament_type": str (schedule,on_capture,immediate)
  "every_s": int
  "reglament_exclusion_time_section": json
  "priority": int
  "regulation": str (immediate, lbt)
  "bs_id": UUID 
  "status": str (created, in_progress, delivered, succeed, failed)
  "task_type": str (time_sync)
  "utc_offeset_s": int
  "protocol":  str (6k7, unbp)
  "time": datetime
]
```

### get base station task api object

method: GET<br/> 
route: '/bs-tasks/<bs_task_id>'<br/>
request:<br/>
```json
    "bs_task_id": UUID
```
response:
```json
  "id": UUID
  "effective_macs": List[int],
  "effective_datetime_from": datetime
  "effective_datetime_to": datetime
  "effective_count": int
  "reglament_type": str (schedule,on_capture,immediate)
  "every_s": int
  "reglament_exclusion_time_section": json
  "priority": int
  "regulation": str (immediate, lbt)
  "bs_id": UUID 
  "status": str (created, in_progress, delivered, succeed, failed)
  "task_type": str (time_sync)
  "utc_offeset_s": int
  "protocol":  str (6k7, unbp)
  "time": datetime
```

### create base station task api object

method: POST<br/> 
route: '/bs-tasks'<br/>
request:<br/>
body:<br/>
```json
    "effective_macs": List[int],
    "effective_datetime_from": datetime
    "effective_datetime_to": datetime
    "effective_count": int
    "reglament_type": str (schedule,on_capture,immediate)
    "every_s": int
    "reglament_exclusion_time_section": json
    "priority": int
    "regulation": str (immediate, lbt)
    "bs_id": UUID 
    "status": str (created, in_progress, delivered, succeed, failed)
    "task_type": str (time_sync)
    "utc_offeset_s": int
    "protocol":  str (6k7, unbp)
    "time": datetime
```
response:
```json
    "id": UUID
    "effective_macs": List[int],
    "effective_datetime_from": datetime
    "effective_datetime_to": datetime
    "effective_count": int
    "reglament_type": str (schedule,on_capture,immediate)
    "every_s": int
    "reglament_exclusion_time_section": json
    "priority": int
    "regulation": str (immediate, lbt)
    "bs_id": UUID 
    "status": str (created, in_progress, delivered, succeed, failed)
    "task_type": str (time_sync)
    "utc_offeset_s": int
    "protocol":  str (6k7, unbp)
    "time": datetime
```

### delete base station task api object

method: DELETE<br/> 
route: '/bs-tasks/<bs_task_id>'<br/>
request:<br/>
```json
    "bs_task_id": UUID
```
response: 200


## base station task log api

### get base station task log api list

method: GET<br/> 
route: '/bs-tasks'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": uuid4, pk
    "task": {
        "id": UUID
        "effective_macs": List[int],
        "effective_datetime_from": datetime
        "effective_datetime_to": datetime
        "effective_count": int
        "reglament_type": str (schedule,on_capture,immediate)
        "every_s": int
        "reglament_exclusion_time_section": json
        "priority": int
        "regulation": str (immediate, lbt)
        "bs_id": UUID 
        "status": str (created, in_progress, delivered, succeed, failed)
        "task_type": str (time_sync)
        "utc_offeset_s": int
        "protocol":  str (6k7, unbp)
        "time": datetime
    }
    "status": enum(created, in_progress, delivered, succeed, failed)
]
```

### get base station task log api object

method: GET<br/> 
route: '/bs-task-logs/<bs_taks_log_id>'<br/>
request:<br/>
```json
    "bs_taks_log_id": UUID
```
response:
```json
    "id": uuid4, pk
    "task": {
        "id": UUID
        "effective_macs": List[int],
        "effective_datetime_from": datetime
        "effective_datetime_to": datetime
        "effective_count": int
        "reglament_type": str (schedule,on_capture,immediate)
        "every_s": int
        "reglament_exclusion_time_section": json
        "priority": int
        "regulation": str (immediate, lbt)
        "bs_id": UUID 
        "status": str (created, in_progress, delivered, succeed, failed)
        "task_type": str (time_sync)
        "utc_offeset_s": int
        "protocol":  str (6k7, unbp)
        "time": datetime
    }
    "status": enum(created, in_progress, delivered, succeed, failed)
```
  

## base station command api

### get base station command api list

method: GET<br/> 
route: '/bs-commands'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": UUID
    "status": str (created, in_progress, delivered, succeed, failed)
    "bs_id": UUID
    "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
    "task_ids": List[int]
]
```

### get base station command api object

method: GET<br/> 
route: '/bs-commands/<bs_command_id>'<br/>
request:<br/>
```json
    "bs_command_id": UUID
```
response:
```json
    "id": UUID
    "status": str (created, in_progress, delivered, succeed, failed)
    "bs_id": UUID
    "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
    "task_ids": List[int]
```

### create base station command api

method: POST<br/> 
route: '/bs-commands'<br/>
request:<br/>
body:<br/>
```json
    "status": str (created, in_progress, delivered, succeed, failed)
    "bs_id": UUID
    "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
    "task_ids": List[int]
```
response:
```json
    "id": UUID
    "status": str (created, in_progress, delivered, succeed, failed)
    "bs_id": UUID
    "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
    "task_ids": List[int]
```

### delete base station command api

method: DELETE<br/> 
route: '/bs-commands/<bs_command_id>'<br/>
request:<br/>
```json
    "bs_command_id": UUID
```
response: 200


## base station command log api

### get base station command log api list

method: GET<br/> 
route: '/bs-commands'<br/>
request:<br/>
```json
    "limit": int
    "offset": int
```
response:
```json
[
    "id": uuid4, pk
    "bs_command": {
        "id": UUID
        "status": str (created, in_progress, delivered, succeed, failed)
        "bs_id": UUID
        "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
        "task_ids": List[int]
    }
    "status": enum(created, in_progress, delivered, succeed, failed)
]
```

### get base station command log api object

method: GET<br/> 
route: '/bs-command-logs/<bs_command_log_id>'<br/>
request:<br/>
```json
    "bs_command_log_id": UUID
```
response:
```json
    "id": uuid4, pk
    "bs_command": {
        "id": UUID
        "status": str (created, in_progress, delivered, succeed, failed)
        "bs_id": UUID
        "command_type": str (delete_downlink_tasks, get_active_downlink_task_ids)
        "task_ids": List[int]
    }
    "status": enum(created, in_progress, delivered, succeed, failed)
```

