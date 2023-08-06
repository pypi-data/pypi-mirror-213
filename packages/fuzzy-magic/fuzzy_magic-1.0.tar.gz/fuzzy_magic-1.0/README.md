# FuzzyMagic

The purpose of this library is to create in the easiest way possible Mamdani Fuzzy Systems. In order to do that, you just need: 

- A file in JSON format that contains each fuzzy set you want to create. The format must be like this: 
```json
{"LinguisticVariable1":{
        "terms": ["you", "are", "awesome"], //mandatory
        "type": "Triangular", //mandatory
        "universe_of_discourse": [0,10] //optional
        }
}
```` 
- A TXT file that contains the rules in Simpful format (although you can create this manually)

Then, you just do this...
```python
    from fuzzy import FuzzyMagic
    FM = FuzzyMagic('path/to/fuzzyset/json', 'path/to/rules/txt')
    FuzzySystem = FM.do_magic()
```

and the magic is done!
