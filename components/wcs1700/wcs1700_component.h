#ifndef WCS1700_COMPONENT_H
#define WCS1700_COMPONENT_H

#include "ACS712.h"
#include "esphome.h"
#include "esphome/core/component.h"       // Contiene la definición de PollingComponent
#include "esphome/components/sensor/sensor.h"  // Contiene la definición de sensor::Sensor


namespace esphome {
namespace wcs1700 {

class WCS1700Sensor : public PollingComponent {
   public:
    WCS1700Sensor(uint8_t pin, float voltage, uint16_t adc_bits, float mV_per_amp, float line_voltage)
        : PollingComponent(5000),
           acs_(pin, voltage, adc_bits, mV_per_amp),
           pin_(pin),
           line_voltage_(line_voltage),
           line_voltage_entity_(nullptr),
           is_ac_(false),
           absolute_(false),
           manual_midpoint_set_(false),
           manual_noise_set_(false),
           samples_(4), // default 100 for dc, 4 for AC
           freq_(50), // default 1000 for dc, 50 for AC
           current_sensor(nullptr),
           power_sensor(nullptr),
           voltage_sensor(nullptr) {},
           line_voltage_sensor(nullptr) {}

    void dump_config() override;
    void setup() override;
    void update() override;

    void set_is_ac(bool is_ac) { this->is_ac_ = is_ac; }
    void set_noisemV(float noisemV) { 
       acs_.setNoisemV(noisemV);
       this->manual_noise_set_ = true;
    }
    void set_noiseSuppress(bool flag) { 
       acs_.suppressNoise(flag); 
       this->noise_suppress_ = flag;
    }
    void set_mid_point(uint16_t mid_point) { 
       acs_.setMidPoint(mid_point); 
       this->manual_midpoint_set_ = true;
    }
    void set_absolute(bool absolute) { absolute_ = absolute; }
    void set_line_voltage(uint8_t voltage) { this->line_voltage_ = voltage; }  
    void set_line_voltage_entity(sensor::Sensor *sensor) { this->line_voltage_entity_ = sensor; }
    void set_samples(uint16_t samples) { this->samples_ = samples; }
    void set_freq(uint16_t freq) { this->freq_ = freq; }

    // Nuevos setters para los sensores configurados desde YAML
    void set_current_sensor(sensor::Sensor *sensor) { current_sensor = sensor; }
    void set_power_sensor(sensor::Sensor *sensor) { power_sensor = sensor; }
    void set_voltage_sensor(sensor::Sensor *sensor) { voltage_sensor = sensor; }
    void set_line_voltage_sensor(sensor::Sensor *sensor) { line_voltage_sensor = sensor; }

   private:
    ACS712 acs_;
    uint8_t pin_;
    float line_voltage_;
    sensor::Sensor *line_voltage_entity_;
    bool is_ac_;
    bool absolute_;
    bool manual_midpoint_set_;
    bool manual_noise_set_;
    bool noise_suppress_;
    uint16_t samples_;
    uint16_t freq_;
    sensor::Sensor *current_sensor;
    sensor::Sensor *power_sensor;
    sensor::Sensor *voltage_sensor;
    sensor::Sensor *line_voltage_sensor;
};

}  // namespace wcs1700
}  // namespace esphome

#endif
