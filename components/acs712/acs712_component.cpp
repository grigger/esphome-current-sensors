#include "acs712_component.h"

namespace esphome {
namespace acs712 {

static const char *const TAG = "acs712";

void ACS712Sensor::dump_config() {
  ESP_LOGCONFIG(TAG, "ACS712\n"
                "  Mode: %s\n"
                "  Pin: %u\n"
                "  MidPoint: %u (%s)\n"
                "  Noise mV: %u (%s)\n"
                "  Noise Suppress: (%s)\n"
                "  Noise Samples Qty: (%u)\n"
                "  Frequency: (%u)\n",
                (this->is_ac_ ? "AC" : "DC"),
                this->pin_,
                this->acs_.getMidPoint(),
                (this->manual_midpoint_set_ ? "manual" : "auto"),
                this->acs_.getNoisemV(),
                (this->manual_noise_set_ ? "manual" : "auto"),
                (this->noise_suppress_ ? "yes" : "no"),
                 this->samples_,
                 this->freq_);

    ESP_LOGCONFIG(TAG, "  -> Current noise mV(instant, recomputed): %.2f", this->acs_.mVNoiseLevel(this->freq_, this->samples_));
}

void ACS712Sensor::setup() {
  // this->set_update_interval(3000);

  if (!this->manual_midpoint_set_) {
    if (this->is_ac_) {
      this->acs_.autoMidPoint(this->freq_, this->samples_);
    } else {
      this->acs_.autoMidPointDC(this->samples_);
    }
  }

  if (!this->manual_noise_set_) {
    this->acs_.setNoisemV(this->acs_.mVNoiseLevel(this->freq_, this->samples_));
  }
}

void ACS712Sensor::update() {
  float amps = 0.0f;

  if (this->is_ac_) {
    //amps = this->acs_.mA_AC(this->freq_, this->samples_) / 1000.0;
    amps = this->acs_.mA_AC_sampling(this->freq_, this->samples_) / 1000.0;
  } else {
    amps = this->acs_.mA_DC(this->samples_) / 1000.0;
  }
  
  if (absolute_) amps = fabsf(amps);

  float effective_line_voltage = this->line_voltage_;
  if (this->line_voltage_entity_ != nullptr && this->line_voltage_entity_->has_state()) {
    float dynamic_line_voltage = this->line_voltage_entity_->get_state();
    if (!std::isnan(dynamic_line_voltage)) {
      effective_line_voltage = dynamic_line_voltage;
    }
  }

  float sensor_output_v = analogReadMilliVolts(this->pin_) / 1000.0f;
  
  current_sensor->publish_state(amps);
  power_sensor->publish_state(amps * effective_line_voltage);
  voltage_sensor->publish_state(sensor_output_v);
  line_voltage_sensor->publish_state(effective_line_voltage);
}


}  // namespace acs712
}  // namespace esphome
