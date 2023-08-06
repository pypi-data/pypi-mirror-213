__version__ = '0.1.2'

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def update_variables(vars_dict):

  var_completer = WordCompleter(list(vars_dict.keys()) + ['exit'])

  def update_var(var_name, value):
    # Function to update the value of a variable
    vars_dict[var_name] = value

  def confirm():
    # Function to ask for confirmation
    confirm_completer = WordCompleter(['yes', 'no'])
    confirm_input = prompt(
      "Are you sure you want to update the variable? (yes/no): ",
      completer=confirm_completer,
      complete_while_typing=True).lower()

    while confirm_input not in ["yes", "no"]:
      print("Invalid input, please enter 'yes' or 'no'.")
      confirm_input = prompt(
        "Are you sure you want to update the variable? (yes/no): ",
        completer=confirm_completer,
        complete_while_typing=True).lower()

    if confirm_input == 'yes':
      return True
    else:
      return False

  while True:
    for k, v in vars_dict.items():
      print(f"{k}: {v}")

    var_name = prompt(
      "Which variable do you want to update? Or type enter to quit: ",
      completer=var_completer,
      complete_while_typing=True)

    if var_name.lower() == '':
      return vars_dict

    if var_name in vars_dict:
      new_value = prompt(f"Enter a new value for {var_name}: ")

      if confirm():
        update_var(var_name, new_value)
        print(f"{var_name} updated successfully.\n")
      else:
        print(f"Update for {var_name} cancelled.\n")
    else:
      print(f"Variable {var_name} not found. Please try again.\n")
