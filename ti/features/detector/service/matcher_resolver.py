"""
Matcher resolver for parsing and evaluating matcher strings from YAML configuration
"""

import re
from typing import Any
from ti.features.detector.service.matchers import Matcher


class MatcherResolver:
    """
    Resolves matcher strings like 'action_is("吃饭")' to callable functions
    """
    
    def __init__(self):
        self.matcher = Matcher()
        
    def resolve_matcher(self, matcher_string: str) -> Any:
        """
        Resolve a matcher string to a callable function
        
        Args:
            matcher_string: String like 'action_is("吃饭")' or 'duration_is_smaller_than(11)'
            
        Returns:
            Callable function that can be used to match ActionUnits
        """
        if not isinstance(matcher_string, str):
            return matcher_string
            
        # Remove whitespace for easier parsing
        clean_string = matcher_string.strip()
        
        # Parse function name and arguments
        match = re.match(r'^(\w+)\((.*)\)$', clean_string)
        if not match:
            raise ValueError(f"Invalid matcher format: {matcher_string}")
            
        function_name = match.group(1)
        args_string = match.group(2)
        
        # Parse arguments
        args = self._parse_arguments(args_string)
        
        # Get the matcher function
        if not hasattr(self.matcher, function_name):
            raise ValueError(f"Unknown matcher function: {function_name}")
            
        matcher_function = getattr(self.matcher, function_name)
        
        # Call the function with arguments to get the actual matcher
        return matcher_function(*args)
    
    def _parse_arguments(self, args_string: str) -> list:
        """
        Parse arguments from string, handling strings, numbers, and None
        """
        if not args_string.strip():
            return []
            
        args = []
        current_arg = ""
        in_string = False
        string_char = None
        
        for char in args_string:
            if not in_string and char in ('"', "'"):
                in_string = True
                string_char = char
                # Don't add the opening quote to current_arg
            elif in_string and char == string_char:
                in_string = False
                # Don't add the closing quote to current_arg
                args.append(current_arg)
                current_arg = ""
            elif not in_string and char == ',':
                if current_arg.strip():
                    args.append(self._convert_arg(current_arg.strip()))
                    current_arg = ""
            else:
                current_arg += char
        
        # Handle last argument
        if current_arg.strip():
            args.append(self._convert_arg(current_arg.strip()))
        
        return args
    
    def _convert_arg(self, arg: str) -> Any:
        """
        Convert argument string to appropriate Python type
        """
        # String literals
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            return arg[1:-1]
        
        # Numbers
        if arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
            return int(arg)
        
        # Floats
        try:
            return float(arg)
        except ValueError:
            pass
        
        # Boolean
        if arg.lower() == 'true':
            return True
        if arg.lower() == 'false':
            return False
        
        # None
        if arg.lower() == 'none':
            return None
        
        # Return as string if no other conversion works
        return arg
    
    def resolve_config(self, config: Any) -> Any:
        """
        Recursively resolve matcher strings in a configuration object
        """
        if isinstance(config, dict):
            return {k: self.resolve_config(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self.resolve_config(item) for item in config]
        elif hasattr(config, '__dict__'):
            # Handle Pydantic models and other objects
            for field_name, field_value in config.__dict__.items():
                if field_name == 'matcher' and isinstance(field_value, str):
                    try:
                        setattr(config, field_name, self.resolve_matcher(field_value))
                    except Exception as e:
                        print(f"Warning: Could not resolve matcher '{field_value}': {e}")
                else:
                    setattr(config, field_name, self.resolve_config(field_value))
            return config
        else:
            return config