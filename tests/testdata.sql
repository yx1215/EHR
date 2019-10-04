INSERT INTO patients (password, name, email, phone_number, gender, height, weight, data_of_birth, emergency_contacts)
VALUES
  ('pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f','alice','alice@nyu.edu','12345678910','female','160.0','45.5','1998-11-18','12345678910'),
  ('pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79','bob','bob@nyu.edu','12345678910','male','170.0','55.0','1998-03-03','12345678910');
