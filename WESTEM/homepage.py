from server.login import log_in_main


def home_page():
    title = "WESTEM"
    about_us = """
    The mission for WESTEM is to aid in the career advancement of women in the
    technology industry, this comprises individuals from many backgrounds like computer
    science, computer engineering, data science and so on. WESTEM caters different resources to women
    in the industry while connecting with experienced mentors. For interactive purposes, this
    system would be compromised of a website.
    """

    #box width
    box_width = 100

    #title box
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + title.center(box_width - 2) + "║")
    print("╚" + "═" * (box_width - 2) + "╝")
    print()

    #about us box
    lines = about_us.strip().split("\n")
    for line in lines:
        print("│" + line.strip().center(box_width - 2) + "│")

    #bottom border
    print("└" + "─" * (box_width - 2) + "┘")


    
def main():

    home_page()

    log_in_main()



if __name__ == "__main__":
    main()
