#!/usr/bin/env python3
"""
Interactive CLI Calculator for Lipi-Lang
లిపి కాలిక్యులేటర్ - Interactive Terminal Version

This provides an interactive command-line interface for the lipi calculator,
integrating with the lipi-lang calculator functions.
"""

import sys
import os

# Add the src directory to the path to import lipi
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from lipi import LipiRuntime, eval_lipi_expr, parse_function_definition

class InteractiveCalculator:
    """Interactive calculator using lipi-lang"""

    def __init__(self):
        """Initialize the calculator with lipi runtime"""
        self.runtime = LipiRuntime()
        self.env = {
            '__runtime__': self.runtime,
            '__functions__': {}
        }
        self.history = []
        self.load_calculator_functions()

    def load_calculator_functions(self):
        """Load calculator function definitions"""

        # Define calculator functions in Python for the environment
        functions_code = [
            # Addition
            ("add", lambda a, b: a + b),
            # Subtraction
            ("subtract", lambda a, b: a - b),
            # Multiplication
            ("multiply", lambda a, b: a * b),
            # Division
            ("divide", lambda a, b: a / b if b != 0 else None),
            # Power
            ("power", lambda a, b: a ** b),
            # Modulo
            ("modulo", lambda a, b: a % b if b != 0 else None),
        ]

        # Add functions to environment
        for name, func in functions_code:
            self.env['__functions__'][name] = {
                'params': ['a', 'b'] if name != 'square_root' else ['n'],
                'body': [],
                'python_func': func
            }

        # Square root function (Newton's method)
        def sqrt_impl(n):
            if n < 0:
                return None
            if n == 0 or n == 1:
                return n

            guess = n / 2
            precision = 0.00001
            iterations = 0
            max_iterations = 100

            while iterations < max_iterations:
                n_div_guess = n / guess
                sum_val = guess + n_div_guess
                better_guess = sum_val / 2
                diff = abs(guess - better_guess)

                if diff < precision:
                    return better_guess

                guess = better_guess
                iterations += 1

            return guess

        self.env['__functions__']['square_root'] = {
            'params': ['n'],
            'body': [],
            'python_func': sqrt_impl
        }

    def call_function(self, func_name, *args):
        """Call a lipi function"""
        if func_name in self.env['__functions__']:
            func = self.env['__functions__'][func_name]
            if 'python_func' in func:
                return func['python_func'](*args)
        return None

    def print_header(self):
        """Print the calculator header"""
        print("\n" + "=" * 70)
        print("🧮 LIPI INTERACTIVE CALCULATOR - లిపి ఇంటరాక్టివ్ కాలిక్యులేటర్")
        print("=" * 70)
        print()

    def print_menu(self):
        """Print the main menu"""
        print("\n" + "-" * 70)
        print("📊 SELECT OPERATION / కార్యకలాపం ఎంచుకోండి:")
        print("-" * 70)
        print()
        print("  BASIC OPERATIONS / ప్రాథమిక కార్యకలాపాలు:")
        print("    1. ➕ Addition / కూడిక")
        print("    2. ➖ Subtraction / వ్యవకలనం")
        print("    3. ✖️  Multiplication / గుణకారం")
        print("    4. ➗ Division / భాగహారం")
        print()
        print("  ADVANCED OPERATIONS / అధునాతన కార్యకలాపాలు:")
        print("    5. ⚡ Power (a^b) / ఘాతాంకం")
        print("    6. 📐 Modulo (a % b) / మాడ్యులో")
        print("    7. √  Square Root / వర్గమూలం")
        print()
        print("  OTHER / ఇతరములు:")
        print("    8. 📋 View History / చరిత్ర చూడండి")
        print("    9. 🗑️  Clear History / చరిత్రను తొలగించండి")
        print("    0. 👋 Exit / నిష్క్రమణ")
        print()
        print("-" * 70)

    def get_number(self, prompt):
        """Get a number from user input"""
        while True:
            try:
                value = input(f"{prompt}: ")
                return float(value)
            except ValueError:
                print("❌ Invalid number. Please try again / చెల్లని సంఖ్య. దయచేసి మళ్లీ ప్రయత్నించండి")
            except (KeyboardInterrupt, EOFError):
                return None

    def perform_calculation(self, operation, operation_name, telugu_name, symbol, num_count=2):
        """Perform a calculation"""
        print(f"\n{symbol} {operation_name} / {telugu_name}")
        print("-" * 70)

        if num_count == 1:
            num = self.get_number("Enter number / సంఖ్య నమోదు చేయండి")
            if num is None:
                return

            result = self.call_function(operation, num)

            if result is None:
                print(f"❌ Error: Invalid operation / దోషం: చెల్లని కార్యకలాపం")
                return

            expression = f"{symbol}{num}"
            print(f"\n✓ Result / ఫలితం: {expression} = {result}")
            self.history.append({
                'expression': expression,
                'result': result,
                'operation': telugu_name
            })

        else:
            num1 = self.get_number("Enter first number / మొదటి సంఖ్య నమోదు చేయండి")
            if num1 is None:
                return

            num2 = self.get_number("Enter second number / రెండవ సంఖ్య నమోదు చేయండి")
            if num2 is None:
                return

            result = self.call_function(operation, num1, num2)

            if result is None:
                if operation == "divide":
                    print("❌ Error: Division by zero / దోషం: సున్నాతో భాగించలేము")
                elif operation == "modulo":
                    print("❌ Error: Modulo by zero / దోషం: సున్నాతో మాడ్యులో చేయలేము")
                else:
                    print("❌ Error: Invalid operation / దోషం: చెల్లని కార్యకలాపం")
                return

            expression = f"{num1} {symbol} {num2}"
            print(f"\n✓ Result / ఫలితం: {expression} = {result}")
            self.history.append({
                'expression': expression,
                'result': result,
                'operation': telugu_name
            })

    def view_history(self):
        """Display calculation history"""
        print("\n" + "=" * 70)
        print("📋 CALCULATION HISTORY / లెక్కింపు చరిత్ర")
        print("=" * 70)

        if not self.history:
            print("\nNo calculations yet / ఇంకా లెక్కలు లేవు")
            return

        print()
        for i, item in enumerate(self.history, 1):
            print(f"{i}. [{item['operation']}] {item['expression']} = {item['result']}")

    def clear_history(self):
        """Clear calculation history"""
        if self.history:
            confirm = input("\nAre you sure? (y/n) / మీరు ఖచ్చితంగా ఉన్నారా? (y/n): ")
            if confirm.lower() == 'y':
                self.history = []
                print("✓ History cleared / చరిత్ర తొలగించబడింది")
        else:
            print("\nHistory is already empty / చరిత్ర ఇప్పటికే ఖాళీగా ఉంది")

    def run(self):
        """Run the interactive calculator"""
        self.print_header()
        print("Welcome! / స్వాగతం!")
        print("This is an interactive bilingual calculator powered by lipi-lang")
        print()

        while True:
            try:
                self.print_menu()
                choice = input("Enter your choice (0-9) / మీ ఎంపిక నమోదు చేయండి (0-9): ").strip()

                if choice == '0':
                    print("\n" + "=" * 70)
                    print("👋 Thank you for using Lipi Calculator!")
                    print("   లిపి కాలిక్యులేటర్ ఉపయోగించినందుకు ధన్యవాదాలు!")
                    print("=" * 70)
                    break

                elif choice == '1':
                    self.perform_calculation('add', 'Addition', 'కూడిక', '+')

                elif choice == '2':
                    self.perform_calculation('subtract', 'Subtraction', 'వ్యవకలనం', '-')

                elif choice == '3':
                    self.perform_calculation('multiply', 'Multiplication', 'గుణకారం', '×')

                elif choice == '4':
                    self.perform_calculation('divide', 'Division', 'భాగహారం', '÷')

                elif choice == '5':
                    self.perform_calculation('power', 'Power', 'ఘాతాంకం', '^')

                elif choice == '6':
                    self.perform_calculation('modulo', 'Modulo', 'మాడ్యులో', '%')

                elif choice == '7':
                    self.perform_calculation('square_root', 'Square Root', 'వర్గమూలం', '√', num_count=1)

                elif choice == '8':
                    self.view_history()

                elif choice == '9':
                    self.clear_history()

                else:
                    print("\n❌ Invalid choice. Please select 0-9 / చెల్లని ఎంపిక. దయచేసి 0-9 ఎంచుకోండి")

            except (KeyboardInterrupt, EOFError):
                print("\n\n" + "=" * 70)
                print("👋 Goodbye! / వీడ్కోలు!")
                print("=" * 70)
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("   Please try again / దయచేసి మళ్లీ ప్రయత్నించండి")

def main():
    """Main entry point"""
    calculator = InteractiveCalculator()
    calculator.run()

if __name__ == "__main__":
    main()
