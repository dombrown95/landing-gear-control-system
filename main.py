from lgcs.controller import LandingGearController

def main():
    controller = LandingGearController()
    controller.command_gear_down()
    controller.command_gear_up()

if __name__ == "__main__":
    main()