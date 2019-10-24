INSERT INTO patients (last_name,first_name,password,email,phone_number,gender,height,weight,data_of_birth,emergency_contacts,medical_his)
VALUES
  ('a', 'a', 'pbkdf2:sha256:150000$GJ2N7qw3$59a29406db35e815977607de5999c36cb5c2d3eb658c0e905804dd1194ec998e','12345@nyu.edu','1234','male','160.0','45.5','1998-11-18','12345','');
INSERT INTO doctors (first_name, last_name, password, email, phone_number, gender, field, date_of_birth, date_of_join)
VALUES
  ('a', 'a', 'pbkdf2:sha256:150000$GJ2N7qw3$59a29406db35e815977607de5999c36cb5c2d3eb658c0e905804dd1194ec998e','123@nyu.edu','1234','male','surg','1998-11-18','2020-11-15'),
  ('bob', 'B', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79',
  'male','12345678910', 'female', 'surg', '2000-01-01', '2019-01-01');

INSERT INTO administrators (first_name, last_name, password, email, phone_number, gender)
VALUES
  ('a', 'a', 'pbkdf2:sha256:150000$GJ2N7qw3$59a29406db35e815977607de5999c36cb5c2d3eb658c0e905804dd1194ec998e','123@nyu.edu','1234','male'),
  ('bob', 'B', 'pbkdf2:sha256:150000$GJ2N7qw3$59a29406db35e815977607de5999c36cb5c2d3eb658c0e905804dd1194ec998e',
  'bob@nyu.edu', '12345', 'male');
