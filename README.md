# CCR scripts 

## Project description

In this repository we present scripts to calculate cross-relaxation rates (CCR) rates
based on MD data

### Scripts description

Code of the project may be divided in two principal parts:
- `ccr_scripts`: directory with python scripts to calculate CCR rates based on MD data
- analysis template: directory with example makefile for calculation dipolar-dipolar NH-CAHA CCR rate. 
  All parameters is specified in `common.mk` file. You may adjust this file for your MD data
    
### Getting started
- specify `common.mk` with your MD data and system
- run make