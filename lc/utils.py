from lc.constants import ACCEPTED_LINES

def check_line_name_validity(lines, accepted_lines=ACCEPTED_LINES):
    individual_lines = lines.split(",")
    for line in individual_lines:
        if line not in accepted_lines:
            return False
    return True
