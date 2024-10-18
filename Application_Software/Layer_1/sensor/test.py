
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_BASELINE_NED
import argparse
import math

def main():
    parser = argparse.ArgumentParser(
        description="Swift Navigation SBP Example.")
    parser.add_argument(
        "-p",
        "--port",
        default=['/dev/ttyUSB0'],
        nargs=1,
        help="specify the serial port to use.")
    args = parser.parse_args()

   # This code block is continuously reading data from a Piksi GPS receiver and processing it to
   # calculate the acceleration in the Earth frame. It uses the SBP protocol to communicate with the
   # receiver and receives messages of type SBP_MSG_BASELINE_NED. It then extracts the necessary data
   # from the message and passes it to the `calculate_acceleration` function to perform the necessary
   # calculations. The acceleration magnitude is then printed to the console. The `try-except` blocks
   # are used to handle any potential errors or interruptions during the data processing.
    try:
        while True:

            # Open a connection to Piksi using the default baud rate (1Mbaud)
            with PySerialDriver(args.port[0], baud=1000000) as driver:
                with Handler(Framer(driver.read, None, verbose=True)) as source:
                    try:
                        for msg, metadata in source.filter(SBP_MSG_BASELINE_NED):
                            x = msg.v_x
                            y = msg.v_y
                            z = msg.v_z
                            pitch = msg.pitch
                            roll = msg.roll
                            heading = msg.heading
                            # Print out the N, E, D coordinates of the baseline
                            print("%.4f,%.4f,%.4f" % (msg.n * 1e-3, msg.e * 1e-3,
                                                    msg.d * 1e-3))
                            
                             # Perform calculations and print the results
                            acceleration = calculate_acceleration(x, y, z, pitch, roll, heading)
                            print("Acceleration:", acceleration)
                    except KeyboardInterrupt:
                        pass
    
    except KeyboardInterrupt:
        pass



def calculate_acceleration(x, y, z, pitch, roll, heading):
    # Convert the accelerometer readings to meters per second squared (m/s²)
    acceleration_x = x * 9.81  # Assuming x-axis calibration and unit conversion
    acceleration_y = y * 9.81  # Assuming y-axis calibration and unit conversion
    acceleration_z = z * 9.81  # Assuming z-axis calibration and unit conversion

    # Convert pitch, roll, and heading from degrees to radians
    pitch_rad = math.radians(pitch)
    roll_rad = math.radians(roll)
    heading_rad = math.radians(heading)

    # Convert acceleration components from the sensor frame to Earth frame
    acceleration_x_earth = acceleration_x * math.cos(pitch_rad) * math.cos(heading_rad) + acceleration_y * (
                math.sin(roll_rad) * math.sin(pitch_rad) * math.cos(heading_rad) - math.cos(roll_rad) * math.sin(
            heading_rad)) + acceleration_z * (
                                       math.cos(roll_rad) * math.sin(pitch_rad) * math.cos(heading_rad) + math.sin(
                                   roll_rad) * math.sin(heading_rad))
    acceleration_y_earth = acceleration_x * math.cos(pitch_rad) * math.sin(heading_rad) + acceleration_y * (
                math.sin(roll_rad) * math.sin(pitch_rad) * math.sin(heading_rad) + math.cos(roll_rad) * math.cos(
            heading_rad)) + acceleration_z * (
                                       math.cos(roll_rad) * math.sin(pitch_rad) * math.sin(heading_rad) - math.sin(
                                   roll_rad) * math.cos(heading_rad))
    acceleration_z_earth = -acceleration_x * math.sin(pitch_rad) + acceleration_y * math.sin(roll_rad) * math.cos(
        pitch_rad) + acceleration_z * math.cos(roll_rad) * math.cos(pitch_rad)

    # Calculate the total acceleration magnitude
    acceleration_magnitude = math.sqrt(acceleration_x_earth ** 2 + acceleration_y_earth ** 2 + acceleration_z_earth ** 2)

    return acceleration_magnitude


if __name__ == "__main__":
    main()