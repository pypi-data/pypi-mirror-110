## Installation

```
pip install plyddl
```

## Usage

```
import plyddl
## init Parser
p = plyddl.Plyddl()
## Parse
p.parse(domain_path, problem_path)
## grounding actions
p.ground_actions()
## grounded actions can be accessed via p.domain.grounded_actions
```
There is no in depth documentation planned so you have to debug or read the source files to get an overview of the structure. 

