from os import path

class AdditionalFunctions():
    options = ["Show rules", "Back"]
    length = len(options)

    def show_rules():
        basepath = path.dirname(__file__)
        rules_path = path.abspath(path.join(basepath, "..", "rules.txt"))
        
        with open(rules_path, "r") as file:
            data = file.read()
            print(data)
        
    functions = [show_rules]