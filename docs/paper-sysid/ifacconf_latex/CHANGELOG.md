# Change log

## [v1.3] - 2022-02-11

### Added

- Change log (this file)

### Changed

- Improve visibility of installation instructions
     - rename `README.txt` to `INSTALL.txt`  
- Fix a bug in `ifacconf.cls`related to `hyperref` 
- Fix a bug in `ifacconf.cls`related to `amsmath`subequations`
- Minor changes in other files in order to update version and date information.

### Removed

- Remove unused files
    - `bifurcation.eps`  
    - `ifacconf-harvard.bst`  

### Fixed

- Package `hyperref` was not not working with `ifacconf.cls`   
      Fixed: hyperreferences are now correctly generated.  
- Subequations (`amsmath`) with more tham twelve equations raised an error.  
      The bug is now fixed.

### Known issues

- *Illegal unit of measure*error when using `hyperref` in the `ifacconf` class  
  This error is raised when unnumbered sections (eg. `\section*` or `\ack`) are used with the `hyperref` package.  
  A workaround can be found [here](https://tex.stackexchange.com/questions/393690/illegal-unit-of-measure-error-when-using-hyperref-in-the-ifacconf-class).


---
## [v1.2] (2011-10-27)

- Update file `COPYRIGHT.md`
- Update sample file `ifanconf.tex`  
    - Show proper format for SI units

## [v1.1] (2008-04-14)

First public release of the ifaconf_latex package.





