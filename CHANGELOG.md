# [0.1.0-alpha.15](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.14...v0.1.0-alpha.15) (2026-04-16)


### Bug Fixes

* add .dockerignore and mount logs as a named volume ([#24](https://github.com/Novanglus96/LenoreSchedule/issues/24)) ([decc51f](https://github.com/Novanglus96/LenoreSchedule/commit/decc51f861683594fc8d7dccc90c1ddd748d8749))

# [0.1.0-alpha.14](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.13...v0.1.0-alpha.14) (2026-04-16)


### Bug Fixes

* create logs directory in Dockerfile so gunicorn app user can write to it ([#23](https://github.com/Novanglus96/LenoreSchedule/issues/23)) ([7bd5cc6](https://github.com/Novanglus96/LenoreSchedule/commit/7bd5cc6fbb38915bfe1c685f31b71da97833b30b))

# [0.1.0-alpha.13](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.12...v0.1.0-alpha.13) (2026-04-16)


### Bug Fixes

* rename Docker image from lenoreschedule_app to lenoreschedule ([#22](https://github.com/Novanglus96/LenoreSchedule/issues/22)) ([0ffc70d](https://github.com/Novanglus96/LenoreSchedule/commit/0ffc70d517904796d07024db85e7a6a7d123ae66))

# [0.1.0-alpha.12](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.11...v0.1.0-alpha.12) (2026-04-16)


### Features

* consolidate frontend, backend, and nginx into single production container ([#21](https://github.com/Novanglus96/LenoreSchedule/issues/21)) ([d48784e](https://github.com/Novanglus96/LenoreSchedule/commit/d48784ea2b11a03074b5a5565550a386d9833cc4))

# [0.1.0-alpha.11](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.10...v0.1.0-alpha.11) (2026-04-16)


### Bug Fixes

* resolve auth before routing to prevent login redirect on page reload ([#20](https://github.com/Novanglus96/LenoreSchedule/issues/20)) ([b03d249](https://github.com/Novanglus96/LenoreSchedule/commit/b03d249e636c787dd0771fe04abf1b7bce2abab6))

# [0.1.0-alpha.10](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.9...v0.1.0-alpha.10) (2026-04-16)


### Features

* add frontend login with session auth and division-scoped access ([#19](https://github.com/Novanglus96/LenoreSchedule/issues/19)) ([105edef](https://github.com/Novanglus96/LenoreSchedule/commit/105edef4fc60678dd137bc30f25498e59da66272))

# [0.1.0-alpha.9](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.8...v0.1.0-alpha.9) (2026-04-16)


### Features

* add UserProfile with division-scoped access control ([#18](https://github.com/Novanglus96/LenoreSchedule/issues/18)) ([eae8637](https://github.com/Novanglus96/LenoreSchedule/commit/eae8637dbba900696be3812adb02dcc920fa441d))

# [0.1.0-alpha.8](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.7...v0.1.0-alpha.8) (2026-04-16)


### Features

* add SQLite compose profile for postgres-free dev ([#17](https://github.com/Novanglus96/LenoreSchedule/issues/17)) ([d71abbf](https://github.com/Novanglus96/LenoreSchedule/commit/d71abbf09355d8277633f269cc5f5213fe23532a))

# [0.1.0-alpha.7](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.6...v0.1.0-alpha.7) (2026-04-16)


### Bug Fixes

* clear start_time, end_time, and location when updating to full-day entry ([#16](https://github.com/Novanglus96/LenoreSchedule/issues/16)) ([35c7317](https://github.com/Novanglus96/LenoreSchedule/commit/35c731714fdbca88da1da8285f7c6e36445c558e))

# [0.1.0-alpha.6](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.5...v0.1.0-alpha.6) (2026-04-16)


### Features

* add ScheduleTemplate model and update CalendarEntry for overrides ([#15](https://github.com/Novanglus96/LenoreSchedule/issues/15)) ([6195422](https://github.com/Novanglus96/LenoreSchedule/commit/6195422e6f7a57cadd299f742724d4a70450d81e))

# [0.1.0-alpha.5](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.4...v0.1.0-alpha.5) (2026-04-16)


### Features

* created payroll info model and services/apis ([#14](https://github.com/Novanglus96/LenoreSchedule/issues/14)) ([8ce5f35](https://github.com/Novanglus96/LenoreSchedule/commit/8ce5f35ea5df529f64af0a874f676dae566a79bb))

# [0.1.0-alpha.4](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.3...v0.1.0-alpha.4) (2026-02-04)


### Bug Fixes

* errors ([46d8444](https://github.com/Novanglus96/LenoreSchedule/commit/46d8444425d7f267f959ec9eb79ba987c7e8563d))


### Features

* added service to calculate date of holiday for a year ([b550f20](https://github.com/Novanglus96/LenoreSchedule/commit/b550f20161e93eb23a7ec4ce89081762c9abee09))
* created holidays ([efd59c3](https://github.com/Novanglus96/LenoreSchedule/commit/efd59c34c6c48b2ef978cec00e1d224543207696))

# [0.1.0-alpha.3](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.2...v0.1.0-alpha.3) (2026-01-30)


### Bug Fixes

* typo in employee router ([9254ec2](https://github.com/Novanglus96/LenoreSchedule/commit/9254ec2c91484051eafb1d6fcdd098b039e31462))


### Features

* added departments ([44cc78c](https://github.com/Novanglus96/LenoreSchedule/commit/44cc78c1b9680d7704e64b8a10c7615918c5bafd))
* added location ([37bc64d](https://github.com/Novanglus96/LenoreSchedule/commit/37bc64d85731c782d27ed2efe5500668c068f565))
* added location, start date, end date to employees ([115b2d6](https://github.com/Novanglus96/LenoreSchedule/commit/115b2d62a7be6f607d9a91e2f41e4a3d2bbdb5d9))
* created employees ([2f86aea](https://github.com/Novanglus96/LenoreSchedule/commit/2f86aeaf3e7ec99530775e6c74c53ebad566d9db))

# [0.1.0-alpha.2](https://github.com/Novanglus96/LenoreSchedule/compare/v0.1.0-alpha.1...v0.1.0-alpha.2) (2026-01-29)


### Bug Fixes

* admin dashboard jazzmin theme ([f08d00c](https://github.com/Novanglus96/LenoreSchedule/commit/f08d00c3865596729510c63380a9c9f4e16f0b4d))
* created groups api ([5a425c9](https://github.com/Novanglus96/LenoreSchedule/commit/5a425c9e2797578382de3ea9253fb3295a6a87e4))
* setup initial colors and logos ([83e63e7](https://github.com/Novanglus96/LenoreSchedule/commit/83e63e7101d925d57b0b51d5cdcd33a4265b137a))

# [0.1.0-alpha.1](https://github.com/Novanglus96/LenoreSchedule/compare/v0.0.1-alpha.1...v0.1.0-alpha.1) (2026-01-29)


### Features

* added groups ([#9](https://github.com/Novanglus96/LenoreSchedule/issues/9)) ([a3a0e61](https://github.com/Novanglus96/LenoreSchedule/commit/a3a0e612b91b08a783e22bfb04c2f1e8c54d3b33))

## [0.0.1-alpha.1](https://github.com/Novanglus96/LenoreSchedule/compare/v0.0.0...v0.0.1-alpha.1) (2026-01-23)


### Bug Fixes

* build issue ([c00975d](https://github.com/Novanglus96/LenoreSchedule/commit/c00975da091b332232f8fcf959a225c431d05b53))
* reddit post workflow ([4205add](https://github.com/Novanglus96/LenoreSchedule/commit/4205add6568012168a17a9ac5168b71088c857b0))
* removed django_q2 ([bc08a1c](https://github.com/Novanglus96/LenoreSchedule/commit/bc08a1c629ef067a7dc08419c54802605689131a))
* removed django_q2 ([a0cc2dd](https://github.com/Novanglus96/LenoreSchedule/commit/a0cc2dd64812ddfdcbd9f7cc8234ceebbe374178))
* setup initial frontend view ([c89c380](https://github.com/Novanglus96/LenoreSchedule/commit/c89c3802460a80aa9857644e6cdad9682a9b9b83))
* update readme ([162048f](https://github.com/Novanglus96/LenoreSchedule/commit/162048f314ff2203ef1f560f5394fd516329fa0c))
* update to build ([250af74](https://github.com/Novanglus96/LenoreSchedule/commit/250af74342f2c59954a507a9d9d336f9187ca61f))

# [1.0.0-alpha.5](https://github.com/Novanglus96/LenoreSchedule/compare/v1.0.0-alpha.4...v1.0.0-alpha.5) (2026-01-23)


### Bug Fixes

* setup initial frontend view ([c89c380](https://github.com/Novanglus96/LenoreSchedule/commit/c89c3802460a80aa9857644e6cdad9682a9b9b83))
