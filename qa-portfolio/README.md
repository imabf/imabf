# QA Testing Portfolio

Hands-on software testing work by **Ahmad Almashhadani**: test case design, bug reporting, API testing with Postman, and SQL data validation.

| Folder | What is inside |
| --- | --- |
| [`test-cases/`](test-cases/login-test-cases.csv) | 22 login-page test cases: positive, negative, boundary, security and usability. Designed with equivalence partitioning and boundary value analysis |
| [`bug-reports/`](bug-reports/README.md) | 5 bug reports from testing a practice login site: steps to reproduce, expected vs actual, severity, impact |
| [`postman/`](postman/) | Postman collection and environment for the public [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) practice API: auth, CRUD and negative tests with assertions (12 requests, 20 assertions) |
| [`sql/`](sql/) | A sample schema and 8 data-quality queries: duplicates, NULLs, orphan records, invalid values, calculation and count checks |

## How to use it

- **Test cases:** open the CSV in Excel or Google Sheets. The Status column is `Fail` for the cases that found a bug (linked to a bug report) and `Not run` for the rest.
- **Postman:** import both files from `postman/`, select the `restful-booker` environment and run the collection in order. Or from the command line:
  ```bash
  npx newman run postman/restful-booker.postman_collection.json -e postman/restful-booker.postman_environment.json
  ```
- **SQL:** run `sql/schema.sql`, then `sql/data-quality-checks.sql` (tested on SQLite). Every check should return zero rows on healthy data; the sample data has planted defects so each one finds something.

## API observations (restful-booker)

Things worth reporting that the Postman collection documents:

- `POST /auth` with wrong credentials returns **200** with `{"reason":"Bad credentials"}` instead of 401.
- `POST /booking` with an empty body returns **500** instead of 400.
- `DELETE /booking/:id` returns **201 Created** instead of 200/204.

## Skills shown

Manual testing · test case design (EP and BVA) · bug reporting · API testing (Postman) · SQL data validation · security-minded test thinking
