# Moment.js for Templater

This reference covers Moment.js features available in Obsidian Templater's `moment` global and `tp.date` functions.

## Common formatting tokens

Used in `tp.date.now(format)` and `moment().format(format)`.

| Symbol | Example                 | Area             |
| ------ | ----------------------- | ---------------- |
| `d`    | `0`..`6`                | **Weekday**      |
| `dd`   | `Su`                    |                  |
| `ddd`  | `Sun`                   |                  |
| `dddd` | `Sunday`                |                  |
| `YY`   | `13`                    | **Year**         |
| `YYYY` | `2013`                  |                  |
| `M`    | `1`..`12` _(Jan is 1)_  | **Month**        |
| `Mo`   | `1st`..`12th`           |                  |
| `MM`   | `01`..`12` _(Jan is 1)_ |                  |
| `MMM`  | `Jan`                   |                  |
| `MMMM` | `January`               |                  |
| `Q`    | `1`..`4`                | **Quarter**      |
| `Qo`   | `1st`..`4th`            |                  |
| `D`    | `1`..`31`               | **Day**          |
| `Do`   | `1st`..`31st`           |                  |
| `DD`   | `01`..`31`              |                  |
| `DDD`  | `1`..`365`              | **Day of year**  |
| `DDDo` | `1st`..`365th`          |                  |
| `DDDD` | `001`..`365`            |                  |
| `w`    | `1`..`53`               | **Week of year** |
| `wo`   | `1st`..`53rd`           |                  |
| `ww`   | `01`..`53`              |                  |

| Symbol | Example    | Area                       |
| ------ | ---------- | -------------------------- |
| `H`    | `0`..`23`  | **24h hour**               |
| `HH`   | `00`..`23` |                            |
| `h`    | `1`..`12`  | **12h hour**               |
| `hh`   | `01`..`12` |                            |
| `m`    | `0`..`59`  | **Minutes**                |
| `mm`   | `00`..`59` |                            |
| `s`    | `0`..`59`  | **Seconds**                |
| `ss`   | `00`..`59` |                            |
| `a`    | `am`       | **AM/PM**                  |
| `A`    | `AM`       |                            |
| `Z`    | `+07:00`   | **Timezone offset**        |
| `ZZ`   | `+0730`    |                            |
| `X`    |            | Unix timestamp             |
| `x`    |            | Millisecond Unix timestamp |

### Common JS manipulations

Use these inside `<%* ... %>` blocks or with the `moment` global.

### Parsing

```js
const m = moment("2013-03-01", "YYYY-MM-DD");
```

### Manipulation

```js
moment().add(1, "day");
moment().subtract(2, "days");
moment().startOf("day");
moment().endOf("month");
```

### Relative time

```js
moment("20111031", "YYYYMMDD").fromNow(); // "12 years ago"
moment().calendar(); // "Today at 12:00 PM"
```

### Localized presets

| Token  | Output (US English)                 |
| ------ | ----------------------------------- |
| `LT`   | 8:30 PM                             |
| `LTS`  | 8:30:25 PM                          |
| `L`    | 09/04/1986                          |
| `l`    | 9/4/1986                            |
| `LL`   | September 4, 1986                   |
| `ll`   | Sep 4, 1986                         |
| `LLL`  | September 4, 1986 8:30 PM           |
| `lll`  | Sep 4, 1986 8:30 PM                 |
| `LLLL` | Thursday, September 4, 1986 8:30 PM |
| `llll` | Thu, Sep 4, 1986 8:30 PM            |

---

## External resources

- [Moment Docs](http://momentjs.com/docs/)
- [Datetime cheatsheet](https://devhints.io/datetime)
