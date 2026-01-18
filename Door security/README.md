# Door Security System

This project was inspired by my mom's phone getting stolen due to a inadequate door security system. It combines face recognition with embedded control to create a
simple automated door locking system.

Users register through a mobile app, which communicates with an Arduino over Bluetooth to control servo motors that operate the lock.

## Design focus
- Keeping the mechanical system simple and reliable
- Using off-the-shelf components thoughtfully rather than over-designing
- Prioritizing robustness over complexity

One key design decision was using dual servo motors to independently control locking and unlocking, avoiding unnecessary mechanical parts while improving reliability.
