# software-design-2022-itmo-spr
Software Design Course Homeworks.

## Elementary Bash.
**Project Structure**:

```bash``` - command line functionality like running bash and reading from std input in a loop

```commandInterface``` - command interface which is implemented in each command (method ```invoke()```).

```commandParse``` - command parser which supports variables assignment (```let``` and ```=```), makes substitutions from environment and distinguishes pipelines and command with their arguments 

```env``` - environment (map of variables and their values within environment with getter and setter)

```test``` - tests for commands, bash, environment and parser

**Commands**: 

* ```wc``` with flags ```-l```, ```-w```, ```-c```

* ```cat``` with flags ```-s```, ```-n```

*  ```exit```

* ```echo```

* ```pwd```


* ```grep``` (in progress)


To launch Bash run ```main.py```

To run tests from Bash folder of the project: ```python3 -m unittest``` 

If getting a error use ```PYTHONPATH="." python3 -m unittest```

GitHub actions were used as CI
