import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID, CONF_PIN, CONF_VOLTAGE, UNIT_AMPERE, UNIT_WATT, UNIT_VOLT,
    ICON_CURRENT_AC, ICON_FLASH,
    DEVICE_CLASS_CURRENT, DEVICE_CLASS_POWER, DEVICE_CLASS_VOLTAGE
)

# Agregamos la dependencia a la biblioteca ACS712
cg.add_library(
    name="ACS712",
    repository="https://github.com/RobTillaart/ACS712.git",
    version=">=0.3.0"
)

CONF_SENSOR_TYPE = "type"
TYPE_AC = "AC"
TYPE_DC = "DC"

DEPENDENCIES = []
#MULTI_CONF = True

# Nombres de los nuevos campos para los sensores hijos
CONF_CURRENT_SENSOR = "current_sensor"
CONF_POWER_SENSOR = "power_sensor"
CONF_VOLTAGE_SENSOR = "voltage_sensor"
CONF_LINE_VOLTAGE_SENSOR = "line_voltage_sensor"

# Constantes de configuración originales
CONF_ADC_BITS = "adc_bits"
CONF_MV_PER_AMP = "mv_per_amp"
CONF_LINE_VOLTAGE = "line_voltage"
CONF_LINE_VOLTAGE_ENTITY = "line_voltage_entity"
CONF_NOISE_MV = "noisemV"
CONF_NOISE_SUPPRESS = "suppress_noise"
CONF_MID_POINT = "mid_point"
CONF_ABSOLUTE = "absolute"
CONF_SAMPLES = "samples_count"
CONF_FREQ = "frequency"

# Define el namespace sin puntos
acs712_ns = cg.esphome_ns.namespace("acs712")
ACS712Sensor = acs712_ns.class_("ACS712Sensor", cg.PollingComponent)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(ACS712Sensor),
    cv.Required(CONF_PIN): cv.int_,
    cv.Required(CONF_VOLTAGE): cv.float_,
    cv.Required(CONF_ADC_BITS): cv.int_,
    cv.Required(CONF_MV_PER_AMP): cv.float_,
    cv.Required(CONF_LINE_VOLTAGE): cv.float_,
    cv.Optional(CONF_LINE_VOLTAGE_ENTITY): cv.use_id(sensor.Sensor),
    cv.Optional(CONF_NOISE_MV): cv.float_,
    cv.Optional(CONF_NOISE_SUPPRESS, default=True): cv.boolean,
    cv.Optional(CONF_SENSOR_TYPE, default=TYPE_DC): cv.one_of(TYPE_AC, TYPE_DC, upper=True),
    cv.Optional(CONF_MID_POINT): cv.int_,
    cv.Optional(CONF_ABSOLUTE, default=False): cv.boolean,
    cv.Optional(CONF_SAMPLES): cv.float_,
    cv.Optional(CONF_FREQ): cv.float_,
    
    # Se definen los schemas para los sensores internos
    cv.Optional(CONF_CURRENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            icon=ICON_CURRENT_AC,
    ),
    cv.Optional(CONF_POWER_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_POWER,
            icon=ICON_FLASH,
    ),
    cv.Optional(CONF_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            icon="mdi:sine-wave"
    ),
    cv.Optional(CONF_LINE_VOLTAGE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            icon="mdi:sine-wave"
    )
}).extend(cv.polling_component_schema("5s"))

async def to_code(config):
    var = cg.new_Pvariable(
        config[CONF_ID],
        config[CONF_PIN],
        config[CONF_VOLTAGE],
        config[CONF_ADC_BITS],
        config[CONF_MV_PER_AMP],
        config[CONF_LINE_VOLTAGE]
    )
    await cg.register_component(var, config)
    
    cg.add(var.set_is_ac(config[CONF_SENSOR_TYPE] == TYPE_AC))
    
    cg.add(var.set_absolute(config[CONF_ABSOLUTE]))
    
    if CONF_NOISE_MV in config:
        cg.add(var.set_noisemV(config[CONF_NOISE_MV]))
    
    cg.add(var.set_noiseSuppress(config[CONF_NOISE_SUPPRESS]))
    
    if CONF_MID_POINT in config:
        cg.add(var.set_mid_point(config[CONF_MID_POINT]))

    if CONF_SAMPLES in config:
        cg.add(var.set_samples(config[CONF_SAMPLES]))
    else:
        if config[CONF_SENSOR_TYPE] == TYPE_AC:
            cg.add(var.set_samples(4))
        else:
            cg.add(var.set_samples(100))

    if CONF_FREQ in config:
        cg.add(var.set_freq(config[CONF_FREQ]))
    else:
        if config[CONF_SENSOR_TYPE] == TYPE_AC:
            cg.add(var.set_freq(50))
        else:
            cg.add(var.set_freq(1000))

    if CONF_LINE_VOLTAGE_ENTITY in config:
        line_voltage_entity = await cg.get_variable(config[CONF_LINE_VOLTAGE_ENTITY])
        cg.add(var.set_line_voltage_entity(line_voltage_entity))
    
    # Registra el sensor de corriente (amperes) si se ha definido en el YAML
    if CONF_CURRENT_SENSOR in config:
        current_sensor = await sensor.new_sensor(config[CONF_CURRENT_SENSOR])
        cg.add(var.set_current_sensor(current_sensor))
    
    # Registra el sensor de potencia (watts) si se ha definido en el YAML
    if CONF_POWER_SENSOR in config:
        power_sensor = await sensor.new_sensor(config[CONF_POWER_SENSOR])
        cg.add(var.set_power_sensor(power_sensor))
    
    # Registra el sensor de potencia (watts) si se ha definido en el YAML
    if CONF_VOLTAGE_SENSOR in config:
        voltage_sensor = await sensor.new_sensor(config[CONF_VOLTAGE_SENSOR])
        cg.add(var.set_voltage_sensor(voltage_sensor))


    if CONF_LINE_VOLTAGE_SENSOR in config:
        voltage_sensor = await sensor.new_sensor(config[CONF_LINE_VOLTAGE_SENSOR])
        cg.add(var.set_line_voltage_sensor(line_voltage_sensor))
