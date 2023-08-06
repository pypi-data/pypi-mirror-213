__version__ = '0.1.0'
def update_variables(vars_dict):
    def update_var(var_name, value):
        # Function to update the value of a variable
        vars_dict[var_name] = value

    def confirm():
        # Function to ask for confirmation
        confirm_input = input("Are you sure you want to update the variable? (yes/no): ").lower()
        while confirm_input not in ["yes", "no"]:
            print("Invalid input, please enter 'yes' or 'no'.")
            confirm_input = input("Are you sure you want to update the variable? (yes/no): ").lower()
        
        if confirm_input == 'yes':
            return True
        else:
            return False

    while True:
        print("Current values:")
        for k, v in vars_dict.items():
            print(f"{k}: {v}")
        
        var_name = input("Which variable do you want to update? Or type 'exit' to quit: ")
        
        if var_name.lower() == 'exit':
            break
        
        if var_name in vars_dict:
            new_value = input(f"Enter a new value for {var_name}: ")
            
            if confirm():
                update_var(var_name, new_value)
                print(f"{var_name} updated successfully.\n")
            else:
                print(f"Update for {var_name} cancelled.\n")
        else:
            print(f"Variable {var_name} not found. Please try again.\n")