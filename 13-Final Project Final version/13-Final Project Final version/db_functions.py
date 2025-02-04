import mysql.connector
__cred = {
    "user":"root",
    "password":"abc123",
    "database":"mhs"
}

def executeStatement(query):
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cnx.close()
    pass


def fetchData(query):
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.fetchall()
    cnx.close()
    return out

def fetchHeading(query):
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def getColumn(table,column):
    query = f'SELECT {column} FROM {table};'
    x = fetchData(query)
    for i in range(len(x)):
        x[i] = x[i][0]
    return x

def getSpecificEmployeeData(jc,pk):
    if jc == 'MD':
        query = f"SELECT * FROM DOCTOR WHERE D_EMPID = '{pk}';"
        pass
    elif jc == 'Nurse':
        query = f"SELECT * FROM NURSE WHERE N_EMPID = '{pk}';"
        pass
    elif jc == 'HCP':
        query = f"SELECT * FROM OTHER_HCP WHERE HCP_EMPID = '{pk}';"
        pass
    else: # Admin
        query = f"SELECT * FROM ADMIN WHERE A_EMPID = '{pk}';"
        pass
    x = fetchData(query)
    tmp = []
    for e in x[0]:
        tmp.append(e)
    return tmp


def getSpecificEmployee(pk):
    query = f"SELECT * FROM EMPLOYEE WHERE EMPID = '{pk}';"
    x = fetchData(query)
    tmp = []
    for e in x[0]:
        tmp.append(e)
    return tmp

# Insurance Company
def getInsuranceCompanyData(insid):
    query = f"SELECT * FROM INSURANCE_COMPANY WHERE INS_ID = {insid};"
    x = fetchData(query)
    tmp = []
    for e in x[0]:
        tmp.append(e)
    return tmp

# Facility Office and OPS
def getFacility(a):
    query = f"SELECT * FROM FACILITY WHERE FACID={a};"
    out = fetchData(query)
    ans = []
    for x in out[0]:
        ans.append(x)
    return ans

def getFacilityHeading():
    query = "SELCT * FROM FACILITY;"
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def getOfficeOPS(fac_id, what):
    if what == 0:
        query = f"SELECT * FROM OFFICE WHERE O_FACID = {fac_id};"
    else:
        query = f"SELECT * FROM OUTPATIENT_SURGERY WHERE OP_FACID = {fac_id};"
    out = fetchData(query)
    ans = []
    for x in out[0]:
        ans.append(x)
    return ans

def getOfficeOPSHeading(what):
    if what == 0:
        query = "SELECT * FROM OFFICE;"
    else:
        query = "SELECT * FROM OUTPATIENT_SURGERY;"
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

# --
def getPhysicianNames():
    query = f"SELECT E.EMPID, E.FNAME, E.LNAME FROM DOCTOR AS D, EMPLOYEE AS E WHERE D.D_EMPID = E.EMPID;"
    x = fetchData(query)
    tmp = []
    for e in x:
        tmp.append([e[0],f'{e[1]} {e[2]}'])
    return tmp

def getFacilityNames():
    query = f"SELECT * FROM FACILITY;"
    x = fetchData(query)
    tmp = []
    for e in x:
        tmp.append([e[0],f"{e[0]} - {e[1]} {e[2]}"])
    return sorted(tmp)

# Employee Assignments
def employeeAssignments():
    query = 'SELECT E.EMPID, E.E_FACID, E.FNAME AS EMPLOYEE_FIRST_NAME, E.LNAME AS EMPLOYEE_LAST_NAME, E.MINIT AS EMPLOYEE_MIDDLE_INITIAL , F.STREET as facility_street, F.CITY as facility_city, F.STATE as facility_state, F.ZIP as facility_zip, F.SIZE as facility_size, F.FTYPE as facility_type FROM EMPLOYEE AS E JOIN FACILITY AS F ON E_FACID = FACID;'
    x = fetchData(query)
    return x

def employeeAssignmentsHeading():
    query = 'SELECT E.EMPID, E.E_FACID, E.FNAME AS EMPLOYEE_FIRST_NAME, E.LNAME AS EMPLOYEE_LAST_NAME, E.MINIT AS EMPLOYEE_MIDDLE_INITIAL , F.STREET as facility_street, F.CITY as facility_city, F.STATE as facility_state, F.ZIP as facility_zip, F.SIZE as facility_size, F.FTYPE as facility_type FROM EMPLOYEE AS E JOIN FACILITY AS F ON E_FACID = FACID;'
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def updateEmployeeAssignment(empid,facid):
    query = f"UPDATE EMPLOYEE SET E_FACID = {facid} WHERE EMPID = {empid};"
    executeStatement(query)
    pass

def getEmployeeFacility(empid):
    query = f"SELECT E_FACID FROM EMPLOYEE WHERE EMPID = {empid};"
    x = fetchData(query)
    return x[0][0]

# Outpatient surgery
def ops():
    query = "SELECT F.*, OS.ROOM_COUNT, OS.P_CODE, OS.DES FROM OUTPATIENT_SURGERY AS OS right join FACILITY AS F on OP_FACID = FACID WHERE F.FTYPE = 'OPS';"
    x = fetchData(query)
    return x

def opsHeading():
    query = "SELECT F.*, OS.ROOM_COUNT, OS.P_CODE, OS.DES FROM OUTPATIENT_SURGERY AS OS right join FACILITY AS F on OP_FACID = FACID WHERE F.FTYPE = 'OPS';"
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

# Office
def office():
    query = '''
    SELECT F.*, O.OFFICE_COUNT
    FROM FACILITY AS F 
    LEFT JOIN OFFICE AS O ON F.FACID = O.O_FACID
    WHERE F.FTYPE = 'Office';
    '''
    x = fetchData(query)
    return x

def officeHeading():
    query = '''
    SELECT F.*, O.OFFICE_COUNT
    FROM FACILITY AS F 
    LEFT JOIN OFFICE AS O ON F.FACID = O.O_FACID
    WHERE F.FTYPE = 'Office';
    '''
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

# Patient
def getPatient():
    query = f'''
    SELECT P.*, CONCAT(E.FNAME, ' ', E.LNAME) AS PRIMARY_PHYSICIAN, IC.INAME FROM 
    PATIENT AS P
    JOIN
    EMPLOYEE AS E ON PRIMARY_D_EMPID = EMPID
    JOIN 
    INSURANCE_COMPANY AS IC
    ON INS_ID = P_INS_ID;
    '''
    x = fetchData(query)
    return x

def getPatientHeading():
    query = f'''
    SELECT P.*, CONCAT(E.FNAME, ' ', E.LNAME) AS PRIMARY_PHYSICIAN, IC.INAME FROM 
    PATIENT AS P
    JOIN
    EMPLOYEE AS E ON PRIMARY_D_EMPID = EMPID
    JOIN 
    INSURANCE_COMPANY AS IC
    ON INS_ID = P_INS_ID;
    '''
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def getAppointment():
    query = f'''
    SELECT
    MA.App_D_EID AS Doctor_ID,
    CONCAT(E.FName,' ',
    E.LName) AS DOCTOR_NAME,
    MA.App_P_ID AS Patient_ID,
    CONCAT(P.FName, ' ',
    P.LName ) AS PATIENT_NAME,
    MA.App_F_ID AS Facility_ID,
    CONCAT(F.Street,' ',
    F.City, ' , ',
    F.State, ' , ',
    F.Zip) AS FACILITY_ADDRESS,
    MA.Date_Time AS Appointment_Date_Time
FROM 
    MAKES_APPOINTMENT MA
JOIN 
    DOCTOR D ON MA.App_D_EID = D.D_EmpID
JOIN 
    EMPLOYEE E ON D.D_EmpID = E.EmpID
JOIN 
    PATIENT P ON MA.App_P_ID = P.P_id
JOIN 
    FACILITY F ON MA.App_F_ID = F.FacID;
    '''
    x = fetchData(query)
    return x

def getAppointmentHeading():
    query = f'''
    SELECT
    MA.App_D_EID AS Doctor_ID,
    CONCAT(E.FName,' ',
    E.LName) AS DOCTOR_NAME,
    MA.App_P_ID AS Patient_ID,
    CONCAT(P.FName, ' ',
    P.LName ) AS PATIENT_NAME,
    MA.App_F_ID AS Facility_ID,
    CONCAT(F.Street,' ',
    F.City, ' , ',
    F.State, ' , ',
    F.Zip) AS FACILITY_ADDRESS,
    MA.Date_Time AS Appointment_Date_Time
FROM 
    MAKES_APPOINTMENT MA
JOIN 
    DOCTOR D ON MA.App_D_EID = D.D_EmpID
JOIN 
    EMPLOYEE E ON D.D_EmpID = E.EmpID
JOIN 
    PATIENT P ON MA.App_P_ID = P.P_id
JOIN 
    FACILITY F ON MA.App_F_ID = F.FacID;
    '''
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans
    
def getAppointmentData(dempid,pid,facid,datetime):
    query = f'''
    SELECT
    MA.App_D_EID AS Doctor_ID,
    CONCAT(E.FName,' ',
    E.LName) AS DOCTOR_NAME,
    MA.App_P_ID AS Patient_ID,
    CONCAT(P.FName, ' ',
    P.LName ) AS PATIENT_NAME,
    MA.App_F_ID AS Facility_ID,
    CONCAT(F.Street,' ',
    F.City, ' , ',
    F.State, ' , ',
    F.Zip) AS FACILITY_ADDRESS,
    MA.Date_Time AS Appointment_Date_Time
    FROM 
        MAKES_APPOINTMENT MA
    JOIN 
        DOCTOR D ON MA.App_D_EID = D.D_EmpID
    JOIN 
        EMPLOYEE E ON D.D_EmpID = E.EmpID
    JOIN 
        PATIENT P ON MA.App_P_ID = P.P_id
    JOIN 
        FACILITY F ON MA.App_F_ID = F.FacID
    WHERE
        D.D_EmpID = {dempid} and
        P.P_id = {pid} and
        F.FacId = {facid} and
        MA.DATE_TIME = {datetime};
    '''
    x = fetchData(query)
    return x

# Employee View
def employee():
    query = '''
    SELECT 
    E.*,
    OH.Job_Title AS Other_HCP_Job_Title,
    N.Certification AS Nurse_Certification,
    A.Job_Title AS Admin_Job_Title,
    D.BC_Date AS Doctor_BC_Date,
    D.Speciality AS Doctor_Speciality
FROM 
    EMPLOYEE E
LEFT JOIN 
    OTHER_HCP OH ON E.EmpID = OH.HCP_EmpID
LEFT JOIN 
    NURSE N ON E.EmpID = N.N_EmpID
LEFT JOIN 
    ADMIN A ON E.EmpID = A.A_EmpID
LEFT JOIN 
    DOCTOR D ON E.EmpID = D.D_EmpID;
    '''
    x = fetchData(query)
    return x


def employeeHeading():
    query = '''
    SELECT 
    E.*,
    OH.Job_Title AS Other_HCP_Job_Title,
    N.Certification AS Nurse_Certification,
    A.Job_Title AS Admin_Job_Title,
    D.BC_Date AS Doctor_BC_Date,
    D.Speciality AS Doctor_Speciality
FROM 
    EMPLOYEE E
LEFT JOIN 
    OTHER_HCP OH ON E.EmpID = OH.HCP_EmpID
LEFT JOIN 
    NURSE N ON E.EmpID = N.N_EmpID
LEFT JOIN 
    ADMIN A ON E.EmpID = A.A_EmpID
LEFT JOIN 
    DOCTOR D ON E.EmpID = D.D_EmpID;
    '''
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

# Get max inv_id
def getMaxInvoiceId():
    query = 'SELECT MAX(INV_ID) FROM INVOICE;'
    x = fetchData(query)[0][0]
    return int(x)

def getInsOfPatient(pid):
    query = f'SELECT P_INS_ID FROM PATIENT WHERE P_ID = {pid}'
    x = fetchData(query)[0][0]
    return int(x)

def getUniqueAppointment():
    query = '''
    SELECT ma.*
    FROM MAKES_APPOINTMENT ma
    LEFT JOIN INVOICE_DETAIL id
        ON ma.App_D_EID = id.Doc_App_ID
        AND ma.App_P_ID = id.Pat_App_ID
        AND ma.App_F_ID = id.Fac_App_ID
        AND ma.Date_Time = id.App_Date_Time
    WHERE id.Inv_id IS NULL;
    '''
    x = fetchData(query)
    return x

def getUniqueAppointmentHeading():
    query = '''
    SELECT ma.*
    FROM MAKES_APPOINTMENT ma
    LEFT JOIN INVOICE_DETAIL id
        ON ma.App_D_EID = id.Doc_App_ID
        AND ma.App_P_ID = id.Pat_App_ID
        AND ma.App_F_ID = id.Fac_App_ID
        AND ma.Date_Time = id.App_Date_Time
    WHERE id.Inv_id IS NULL;
    '''
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def getDateTime():
    query = f'SELECT NOW();'
    x = fetchData(query)[0][0]
    return x

def getDate():
    query = f'select curdate();'
    x = fetchData(query)[0][0]
    return x

# Everything invoice
def getEverythingInvoice():
    query = 'select id.* from invoice_detail as id, invoice i where i.inv_id = id.inv_id;'
    x = fetchData(query)
    return x


def getEverythingInvoiceHeading():
    query = 'select id.* from invoice_detail as id, invoice i where i.inv_id = id.inv_id;'
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans
# Get patient id
def getPatientId():
    query = 'SELECT P_ID FROM PATIENT;'
    x = fetchData(query)
    tmp = []
    for y in x:
        tmp.append(y[0])
    return tmp

# Get doctor id
def getDoctorId():
    query = 'SELECT D_EMPID FROM DOCTOR;'
    x = fetchData(query)
    tmp = []
    for y in x:
        tmp.append(y[0])
    return tmp

def getPatientData(pid):
    query = f"SELECT * FROM PATIENT WHERE P_ID = {pid};"
    x = fetchData(query)
    tmp = []
    for e in x[0]:
        tmp.append(e)
    return tmp

# Get insruance id
def getInsuranceId():
    query = 'SELECT INS_ID FROM INSURANCE_COMPANY;'
    x = fetchData(query)
    tmp = []
    for y in x:
        tmp.append(y[0])
    return tmp


# INSERT UPDATE DELETE FOR ALL TABLES
# EMPLOYEE
def insertEmployee(data):
    query = f"INSERT INTO EMPLOYEE VALUES ({data[0]}, '{data[1]}', {data[2]}, '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', '{data[8]}', '{data[9]}', {data[10]}, '{data[11]}', '{data[12]}');"
    executeStatement(query)
    pass
def updateEmployee(data):
    query = f"UPDATE EMPLOYEE SET SSN='{data[1]}', E_FACID={data[2]}, STREET='{data[3]}', CITY='{data[4]}', STATE='{data[5]}', ZIP='{data[6]}', FNAME='{data[7]}', LNAME='{data[8]}', MINIT='{data[9]}', SALARY={data[10]}, HIREDATE='{data[11]}', JOBCLASS='{data[12]}' WHERE EMPID = {data[0]}"
    executeStatement(query)
    pass
def deleteEmployee(empid):
    query = f"DELETE FROM EMPLOYEE WHERE EMPID = {empid};"
    executeStatement(query)
    pass

# OTHER HCP
def insertHCP(data):
    query = f"INSERT INTO OTHER_HCP VALUES({data[0]},'{data[1]}');"
    executeStatement(query)
    pass
def updateHCP(data):
    query = f"UPDATE OTHER_HCP SET JOB_TITLE = '{data[1]}' WHERE HCP_EMPID = {data[0]}"
    executeStatement(query)
    pass

# Nurse
def insertNurse(data):
    query = f"INSERT INTO NURSE VALUES({data[0]},'{data[1]}');"
    executeStatement(query)
    pass
def updateNurse(data):
    query = f"UPDATE NURSE SET CERTIFICATION = '{data[1]}' WHERE N_EMPID = {data[0]}"
    executeStatement(query)
    pass

# Admin
def insertAdmin(data):
    query = f"INSERT INTO ADMIN VALUES({data[0]},'{data[1]}');"
    executeStatement(query)
    pass
def udpateAdmin(data):
    query = f"UPDATE ADMIN SET JOB_TITLE='{data[1]}' WHERE A_EMPID = {data[0]}"
    executeStatement(query)
    pass

# Doctor
def insertDoctor(data):
    query = f"INSERT INTO DOCTOR VALUES({data[0]},'{data[1]}','{data[2]}');"
    executeStatement(query)
    pass
def updateDoctor(data):
    query = f"UPDATE DOCTOR SET BC_DATE = '{data[1]}', SPECIALITY='{data[2]}' WHERE D_EMPID = {data[0]}"
    executeStatement(query)
    pass

# Treats
def insertTreats(data):
    query = f"INSERT INTO TREATS VALUES({data[0]},{data[1]});"
    executeStatement(query)
    pass
def updateTreats(data,flag):
    if flag:
        query = f"UPDATE TREATS SET D_EMPID = {data[0]} WHERE P_ID = {data[1]}"
        executeStatement(query)
    else:
        query = f"UPDATE TREATS SET D_EMPID = {data[1]} WHERE P_ID = {data[0]}"
        executeStatement(query)
    pass
def deleteTreats(d_empid,p_id):
    query = f"DELETE FROM TREATS WHERE D_EMPID = {d_empid} AND P_ID = {p_id}"
    executeStatement(query)
    pass

# Patient
def insertPatient(data):
    query = f"INSERT INTO PATIENT VALUES({data[0]}, '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', {data[8]}, {data[9]});"
    executeStatement(query)
    pass
def updatePatient(data):
    query = f"UPDATE PATIENT SET PRIMARY_D_EMPID = '{data[1]}', P_INS_ID = '{data[2]}', STATE = '{data[3]}', ZIP = '{data[4]}', FNAME = '{data[5]}', MINIT = '{data[6]}', LNAME = '{data[7]}', STREET = '{data[8]}', CITY = '{data[9]}' WHERE P_ID = {data[0]} ;"
    executeStatement(query)
    pass
def deletePatient(p_id):
    query = f"DELETE FROM PATIENT WHERE P_ID = {p_id};"
    executeStatement(query)
    pass

# Insurance Company
def insertInsuranceCompany(data):
    query = f"INSERT INTO INSURANCE_COMPANY VALUES({data[0]}, '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}');"
    executeStatement(query)
    pass
def updateInsuranceCompany(data):
    query = f"UPDATE INSURANCE_COMPANY SET INAME = '{data[1]}', STREET = '{data[2]}', CITY = '{data[3]}', STATE = '{data[4]}', ZIP = '{data[5]}' WHERE INS_ID = {data[0]}"
    executeStatement(query)
    pass
def deleteInsuranceCompany(ins_id):
    query = f"DELETE FROM INSURANCE_COMPANY WHERE INS_ID = {ins_id}"
    executeStatement(query)
    pass

# Invoice
def insertInvoice(data):
    query = f"INSERT INTO INVOICE VALUES({data[0]}, {data[1]}, '{data[2]}', {data[3]});"
    executeStatement(query)
    pass
def updateInvoice(data):
    query = f"UPDATE INVOICE SET INV_INS_ID = {data[1]}, INV_DATE = '{data[2]}', INV_AMT = {data[3]} WHERE INV_ID = {data[0]}"
    executeStatement(query)
    pass
def deleteInvoice(inv_id):
    query = f"DELTE FROM INVOICE WHERE INV_ID = {inv_id};"
    executeStatement(query)
    pass

# Invoice detail
def insertInvoiceDetail(data):
    query = f"INSERT INTO INVOICE_DETAIL VALUES({data[0]}, {data[1]}, {data[2]}, {data[3]}, '{data[4]}', {data[5]});"
    print(query)
    executeStatement(query)
    pass
def updateInvoiceDetail(data):
    query = f"UPDATE INVOICE_DETAIL SET  COST = {data[5]} WHERE INV_ID = {data[0]} AND DOC_APP_ID = {data[1]} AND PAT_APP_ID = {data[2]} AND FAC_APP_ID = {data[3]} AND DATE_TIME = '{data[4]}';"
    executeStatement(query)
    pass
def deleteInvoiceDetail(inv_id,doc_app_id,pat_app_id,fac_app_id,date_time):
    query = f"DELETE FROM INVOICE_DETAIL WHERE INV_ID = {inv_id}, DOC_APP_ID = {doc_app_id}, PAT_APP_ID = {pat_app_id}, FAC_APP_ID = {fac_app_id}, DATE_TIME = '{date_time}';"
    executeStatement(query)
    pass

# Office
def insertOffice(data):
    query = f"INSERT INTO OFFICE VALUES({data[0]},{data[1]});"
    executeStatement(query)
    pass
def updateOffice(data):
    query = f"UPDATE OFFICE SET OFFICE_COUNT = {data[1]} WHERE O_FACID = {data[0]};"
    executeStatement(query)
    pass
def deleteOffice(o_facid):
    query = f"DELETE FROM OFFICE WHERE O_FACID = {o_facid};"
    executeStatement(query)
    pass

# Outpatient Surgery
def insertOutpatientSurgery(data):
    query = f"INSERT INTO OUTPATIENT_SURGERY VALUES({data[0]}, {data[1]}, '{data[2]}', '{data[3]}');"
    executeStatement(query)
    pass
def updateOutpatientSurgery(data):
    query = f"UPDATE OUTPATIENT_SURGERY SET ROOM_COUNT = {data[1]}, P_CODE = '{data[2]}', DES = '{data[3]}' WHERE OP_FACID = {data[0]};"
    print(query)
    executeStatement(query)
    pass
def deleteOutpatientSurgery(op_facid):
    query = f"DELETE FROM OUTPATIENT_SURGERY WHERE OP_FACID = {op_facid};"
    executeStatement(query)
    pass

# Facility
def insertFacility(data):
    query = f"INSERT INTO FACILITY VALUES({data[0]}, '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', {data[5]}, '{data[6]}');"
    # print(query)
    executeStatement(query)
    pass
def updateFacility(data):
    query = f"UPDATE FACILITY SET STREET = '{data[1]}', CITY = '{data[2]}', STATE = '{data[3]}', ZIP = '{data[4]}', SIZE = {data[5]}, FTYPE = '{data[6]}' WHERE FACID = {data[0]}"
    executeStatement(query)
    pass
def deleteFacility(facid):
    query = f"DELETE FROM FACILITY WHERE FACID = {facid};"
    executeStatement(query)
    pass

# Makes Appointment
def insertMakesAppointment(data):
    query = f"INSERT INTO MAKES_APPOINTMENT VALUES({data[0]}, {data[1]}, {data[2]}, '{data[3]}');"
    executeStatement(query)
    pass
def updateMakesAppointment(data):
    query = f"UPDATE MAKES_APPOINTMENT SET "
    executeStatement(query)
    pass
def deleteMakesAppointment(app_d_id,app_p_id,app_f_id,date_time):
    query = f"DELETE FROM MAKES_APPOINTMENT WHERE APP_D_EID = {app_d_id} AND APP_P_ID = {app_p_id} AND APP_F_ID = {app_f_id} AND DATE_TIME = '{date_time}';"
    executeStatement(query)
    pass


def getData(table):
    out = fetchData(f"SELECT * FROM {table};")
    ans = []
    for data in out:
        tmp = []
        for y in data:
            tmp.append(y)
        ans.append(tmp)
    return ans

def tableHeading(table):
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def tableHeadingAnswer(query):
    cnx = mysql.connector.connect(**__cred)
    cursor = cnx.cursor()
    cursor.execute(query)
    out = cursor.description
    ans = []
    for x in out:
        ans.append(x[0])
    cnx.close()
    return ans

def getDataAnswer(query):
    out = fetchData(query)
    ans = []
    for data in out:
        tmp = []
        for y in data:
            tmp.append(y)
        ans.append(tmp)
    return ans

def __getQueryAnswer(num,date):
    if num == 1:
        query1 = f'''
        SELECT 
    F.FacID AS 'Facility ID',
    SUM(ID.Cost) AS 'Revenue'
FROM 
    FACILITY F
JOIN 
    MAKES_APPOINTMENT MA ON F.FacID = MA.App_F_ID
JOIN 
    INVOICE_DETAIL ID ON MA.App_D_EID = ID.Doc_App_ID AND MA.App_P_ID = ID.Pat_App_ID AND MA.App_F_ID = ID.Fac_App_ID AND MA.Date_Time = ID.App_Date_Time
WHERE 
    DATE(MA.Date_Time) = '{date[0]}'
GROUP BY 
    F.FacID
WITH ROLLUP;
'''
        return query1
    if num == 2:
        query2 = f'''
SELECT 
    MA.App_D_EID AS Physician_ID,
    MA.App_P_ID AS Patient_ID,
    MA.Date_Time AS Appointment_Date_Time
FROM MAKES_APPOINTMENT MA
WHERE DATE(MA.Date_Time) = '{date[0]}' AND MA.App_D_EID = {date[1]};
'''
        return query2
    if num == 3:
        sample = f'select ftype from facility where facid = {date[2]};'
        x = fetchData(sample)
        if x[0][0] == 'Office':
            query3 = f'''
SELECT 
	MA.APP_F_ID AS 'FACILITY ID',
    MA.Date_Time AS Appointment_Date_Time,
    D.D_EMPID as 'Physician ID',
    CONCAT(E.FName,' ',
    E.LName) AS 'Physician Name',
    P.P_ID AS 'Patient ID',
    CONCAT(P.FName, ' ',
    P.LName) AS 'Patient Name'
FROM 
    MAKES_APPOINTMENT MA
JOIN 
    OFFICE O ON MA.App_F_ID = O.O_FacID
JOIN
    PATIENT P ON MA.App_P_ID = P.P_id
JOIN
    DOCTOR D ON MA.App_D_EID = D.D_EmpID
JOIN
    EMPLOYEE E ON D.D_EmpID = E.EmpID
WHERE 
    MA.Date_Time BETWEEN '{date[0]} 00:00:00' AND '{date[1]} 23:59:59' AND MA.App_F_ID = {date[2]};

            '''
            pass
        else:
            query3 = f'''
SELECT 
	MA.APP_F_ID AS 'FACILITY ID',
    MA.Date_Time AS Appointment_Date_Time,
    D.D_EMPID as 'Physician ID',
    CONCAT(E.FName,' ',
    E.LName) AS 'Physician Name',
    P.P_ID AS 'Patient ID',
    CONCAT(P.FName, ' ',
    P.LName) AS 'Patient Name',
    O.DES AS 'Description'
FROM 
    MAKES_APPOINTMENT MA
JOIN 
    OUTPATIENT_SURGERY O ON MA.App_F_ID = O.OP_FacID
JOIN
    PATIENT P ON MA.App_P_ID = P.P_id
JOIN
    DOCTOR D ON MA.App_D_EID = D.D_EmpID
JOIN
    EMPLOYEE E ON D.D_EmpID = E.EmpID
WHERE 
    MA.Date_Time BETWEEN '{date[0]} 00:00:00' AND '{date[1]} 23:59:59' AND MA.App_F_ID = {date[2]};
'''
        return query3
    if num == 4:
        query4 = f'''
SELECT 
    DATE(MA.Date_Time) AS Date,
    SUM(ID.Cost) AS Total_Revenue
FROM 
    MAKES_APPOINTMENT MA
JOIN 
    INVOICE_DETAIL ID ON MA.App_D_EID = ID.Doc_App_ID AND MA.App_P_ID = ID.Pat_App_ID AND MA.App_F_ID = ID.Fac_App_ID AND DATE(MA.Date_Time) = DATE(ID.App_Date_Time)
WHERE 
    YEAR(MA.Date_Time) = 2024 AND MONTH(MA.Date_Time) = {date[0]}
GROUP BY 
    DATE(MA.Date_Time)
ORDER BY 
    Total_Revenue DESC
LIMIT 5;
'''
        return query4
    if num  == 5:
        query5 = f'''
SELECT I.Inv_Ins_id AS Insurance_Company_ID,
    AVG(I.Inv_amt) AS Average_Daily_Revenue
FROM INVOICE I
WHERE 
    I.Inv_date BETWEEN '{date[0]}' AND '{date[1]}'
GROUP BY 
    I.Inv_Ins_id;
'''
        return query5


def getAnswer(num,*date):
    query = __getQueryAnswer(num,date)
    if num == 1:
        return [tableHeadingAnswer(query),getDataAnswer(query)]
    
    elif num == 2:
        return [tableHeadingAnswer(query),getDataAnswer(query)]
    elif num == 3:
        return [tableHeadingAnswer(query),getDataAnswer(query)]
    elif num == 4:
        return [tableHeadingAnswer(query),getDataAnswer(query)]
    elif num == 5:
        return [tableHeadingAnswer(query),getDataAnswer(query)]
    else:
        return "error"

def getICInvoice(date = 0):
    if date == 0:
        query1 = '''
SELECT 
    I.Inv_date AS 'Invoice Date',
    IC.IName AS 'Insurance Company',
    CONCAT(P.FName, ' ',
    P.LName) AS 'Patient Name',
    SUM(ID.Cost) AS 'Patient Subtotal'
FROM 
    INVOICE I
JOIN 
    INVOICE_DETAIL ID ON I.Inv_id = ID.Inv_id
JOIN 
    INSURANCE_COMPANY IC ON I.Inv_Ins_id = IC.Ins_ID
JOIN 
    PATIENT P ON ID.Pat_App_ID = P.P_id
WHERE 
    I.Inv_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
GROUP BY 
    I.Inv_date, IC.IName, P.FName, P.LName;
'''
        query2 = '''
SELECT 
    I.Inv_date AS 'Invoice Date',
    IC.IName AS 'Insurance Company',
    SUM(I.Inv_amt) AS 'Total Amount'
FROM 
    INVOICE I
JOIN 
    INSURANCE_COMPANY IC ON I.Inv_Ins_id = IC.Ins_ID
WHERE 
    I.Inv_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
GROUP BY 
    I.Inv_date, IC.IName;
'''
    else:
        query1 = f'''
SELECT 
    I.Inv_date AS 'Invoice Date',
    IC.IName AS 'Insurance Company',
    CONCAT(P.FName, ' ',
    P.LName) AS 'Patient Name',
    SUM(ID.Cost) AS 'Patient Subtotal'
FROM 
    INVOICE I
JOIN 
    INVOICE_DETAIL ID ON I.Inv_id = ID.Inv_id
JOIN 
    INSURANCE_COMPANY IC ON I.Inv_Ins_id = IC.Ins_ID
JOIN 
    PATIENT P ON ID.Pat_App_ID = P.P_id
WHERE 
    I.Inv_date = '{date}'
GROUP BY 
    I.Inv_date, IC.IName, P.FName, P.LName;
'''
        query2 = f'''
SELECT 
    I.Inv_date AS 'Invoice Date',
    IC.IName AS 'Insurance Company',
    SUM(I.Inv_amt) AS 'Total Amount'
FROM 
    INVOICE I
JOIN 
    INSURANCE_COMPANY IC ON I.Inv_Ins_id = IC.Ins_ID
WHERE 
    I.Inv_date = '{date}'
GROUP BY 
    I.Inv_date, IC.IName;
'''
    q1 = getDataAnswer(query1)
    q2 = getDataAnswer(query2)
    qh1 = fetchHeading(query1)
    qh2 = fetchHeading(query2)
    heading1 = 'Patient Subtotal'
    heading2 = 'Insurance Company Total'
    return [[heading1,qh1,q1], [heading2,qh2,q2]]