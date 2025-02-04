from flask import Flask, render_template, redirect, url_for
from flask import request
import db_functions as db

app = Flask(__name__)

@app.route("/")
def home():
    return redirect('employee')

@app.route('/employee')
def employee():
    return render_template('employee_home.html')

@app.route('/employee/<type>', methods=('GET','POST'))
def employeeInsertUpdate(type):
    efacid = db.getColumn('facility','facid')
    empid = sorted(db.getColumn('employee','empid'))
    extradata = ['' for _ in range(3)]
    data = ['' for _ in range(13)]
    if request.method == 'POST':
        if request.form['btn'] == 'Delete':
            empid_del = request.form['empid_u']
            db.deleteEmployee(empid_del)
            return redirect('/view/1/employee')
        
        if request.form['btn'] == 'Search': # Update
            empid_tmp = request.form['empid_u']
            data = db.getSpecificEmployee(empid_tmp)
            extradata = db.getSpecificEmployeeData(data[12],data[0])
            extradata.append('')
            update_flag = 1
            return render_template('employee_iu.html',activeclass=1,efacid=efacid,data = data,empid=empid,extradata=extradata,updateflag=1)

        if request.form['btn'] == 'Submit' or request.form['btn'] == 'Update': # Insert
            if request.method == 'POST':
                data = [
                    request.form['empid'],
                    request.form['ssn'],
                    request.form['e_facid'],
                    request.form['street'],
                    request.form['city'],
                    request.form['state'],
                    request.form['zip'],
                    request.form['fname'],
                    request.form['lname'],
                    request.form['minit'],
                    request.form['salary'],
                    request.form['hiredate'],
                    request.form['jobclass'],
                    request.form['job_title'], #13
                    request.form['certification'],
                    request.form['bc_date'],
                    request.form['speciality']
                ]
                if request.form['btn'] == 'Update':
                    # Update
                    db.updateEmployee(data)
                    jc = request.form['jobclass']
                    if jc == 'MD':
                        db.updateDoctor([data[0],data[15],data[16]])
                        pass
                    elif jc == 'Nurse':
                        db.updateNurse([data[0],data[14]])
                        pass
                    elif jc == 'HCP':
                        db.updateHCP([data[0],data[13]])
                        pass
                    else: # Admin
                        db.udpateAdmin([data[0],data[13]])
                        pass
                    pass
                else:
                    # Insert
                    db.insertEmployee(data)
                    jc = request.form['jobclass']
                    if jc == 'MD':
                        db.insertDoctor([data[0],data[15],data[16]])
                        pass
                    elif jc == 'Nurse':
                        db.insertNurse([data[0],data[14]])
                        pass
                    elif jc == 'HCP':
                        db.insertHCP([data[0],data[13]])
                        pass
                    else: # Admin
                        db.insertAdmin([data[0],data[13]])
                        pass
                    pass
                return redirect('/view/1/employee')
    return render_template('employee_iu.html',activeclass=1,efacid=efacid,data=data,empid=empid,extradata=extradata,updateflag=0)

@app.route('/medical_offices',methods=('GET','POST'))
def medical_offices():
    ofacids = sorted(db.getColumn('facility','facid'))
    fac_facid = sorted(db.getColumn('facility','facid'))
    extradata = ['' for _ in range(4)]
    data = ['' for _ in range(11)]
    if request.method == 'POST':
        btnname = request.form['btn']
        data = [
            request.form['facid'],
            request.form['street'],
            request.form['city'],
            request.form['state'],
            request.form['zip'],
            request.form['size'],
            request.form['ftype']
        ]
        extradata = [
            request.form['facid'],
            request.form['office_count'],
            request.form['room_count'],
            request.form['p_code'],
            request.form['description']
        ]
        if btnname == 'Delete': # Delete
            db.deleteFacility(request.form['facid_u'])
            return redirect('/view/1/office')

        if btnname == 'Submit': # Insert
            db.insertFacility(data)
            if request.form['ftype'] == 'OPS':
                db.insertOutpatientSurgery([extradata[0],extradata[2],extradata[3],extradata[4]])
                pass
            else:
                db.insertOffice([extradata[0],extradata[1]])
                pass
            return redirect('/view/1/office')

        if btnname == 'Search': # Update (data to form)
            facid_tmp = request.form['facid_u']
            data = db.getFacility(facid_tmp)
            ogftype = data[6]
            extradataOffice = ['' for _ in range(2)]
            extradataOPS = ['' for _ in range(4)]
            if data[6] == 'Office':
                extradataOffice = db.getOfficeOPS(facid_tmp,0)
            else:
                extradataOPS = db.getOfficeOPS(facid_tmp,1)
            extradata = [extradataOffice[0],extradataOffice[1],extradataOPS[1],extradataOPS[2],extradataOPS[3]]
            return render_template('medical_offices_iu.html',activeclass=1,data=data,extradata=extradata,facids=ofacids,fac_facid=fac_facid,updateflag=1)

        if btnname == 'Update': # Actual update
            facid_tmp = data[0]
            datatmp = db.getFacility(facid_tmp)
            ogftype = datatmp[6]
            tmpdata = data[6]
            db.updateFacility(data)
            if request.form['ftype'] == 'OPS':
                if ogftype != tmpdata:
                    db.insertOutpatientSurgery([extradata[0],extradata[2],extradata[3],extradata[4]])
                else:
                    db.updateOutpatientSurgery([extradata[0],extradata[2],extradata[3],extradata[4]])
                pass
            else:
                if ogftype != tmpdata:
                    db.insertOffice([extradata[0],extradata[1]])
                else:
                    db.updateOffice([extradata[0],extradata[1]])
                pass
            if ogftype != tmpdata:
                if tmpdata == 'Office':
                    # Delete OPS
                    db.deleteOutpatientSurgery(data[0])
                else:
                    # Delete Office
                    db.deleteOffice(data[0])
            if tmpdata == 'Office':
                return redirect('/view/1/office')
            else:
                return redirect('/view/1/outpatient_surgery')

        pass
    return render_template('medical_offices_iu.html',activeclass = 1,data=data,extradata=extradata, facids = ofacids, fac_facid = fac_facid)

@app.route('/employee_assignments',methods=('GET','POST'))
def employeeAssignments():
    data = ['','']
    facid = sorted(db.getColumn('facility','facid'))
    empid = sorted(db.getColumn('employee','empid'))
    if request.method == 'POST':
        if request.form['btn'] == 'Re Search':
            return render_template('employee_assignment_iu.html',activeclass = 1, data = data, facid = facid, empid = empid)
        if request.form['btn'] == 'Search':
            curr_empid = request.form['empid']
            curr_facid = db.getEmployeeFacility(curr_empid)
            return render_template('employee_assignment_iu.html',activeclass = 1, data = data, facid = facid, empid = empid, showflag = 1, curr_empid = curr_empid,curr_facid=curr_facid)
        if request.form['btn'] == 'Re Assign':
            empid_new = request.form['empid']
            facid_new = request.form['facid']
            db.updateEmployeeAssignment(empid_new,facid_new)
            return redirect('/view/1/employeeassignment')
    return render_template('employee_assignment_iu.html',activeclass = 1, data = data, facid = facid, empid = empid)

@app.route('/insurance_company',methods=('GET','POST'))
def insuranceCompany():
    data = ['' for _ in range(6)]
    insid = db.getColumn('insurance_company','ins_id')
    if request.method == 'POST':
        btnname = request.form['btn']
        data = [
            request.form['insid'],
            request.form['name'],
            request.form['street'],
            request.form['city'],
            request.form['state'],
            request.form['zip']
        ]
        if btnname == 'Delete':
            db.deleteInsuranceCompany(request.form['insid_u'])
            return redirect('/view/1/insurance_company')
        if btnname == 'Search':
            insid_u = request.form['insid_u']
            data = db.getInsuranceCompanyData(insid_u)
            return render_template('insurance_company_iu.html',activeclass=1,data=data,insid=insid,updateflag=1)
        if btnname == 'Submit':
            db.insertInsuranceCompany(data)
            return redirect('/view/1/insurance_company')
        if btnname == 'Update':
            db.updateInsuranceCompany(data)
            return redirect('/view/1/insurance_company')
        pass
    return render_template('insurance_company_iu.html',activeclass=1,data=data,insid=insid)

@app.route('/management')
def management():
    return render_template('management_home.html')

@app.route('/patient')
def patient():
    return render_template('patient_home.html')

@app.route('/patientiu',methods=('GET','POST'))
def patientiu():
    docid = sorted(db.getDoctorId())
    patid = sorted(db.getPatientId())
    insid = sorted(db.getInsuranceId())
    data = ['' for _ in range(10)]
    if request.method == 'POST':
        btnname = request.form['btn']
        if btnname == 'Delete': # Delete record
            db.deletePatient(request.form['patid_u'])
            return redirect('/view/2/patient') # Redirect to view
        if btnname == 'Search': # Get data
            data = db.getPatientData(request.form['patid_u'])
            return render_template('patient_iu.html',updateflag = 1,activeclass=2,data = data,docid=docid,patid=patid,insid=insid) # Redirect to same template with different data value
        if btnname == 'Submit': # Insert data
            data = [
            request.form['patid'],
            request.form['fname'],
            request.form['lname'],
            request.form['minit'],
            request.form['street'],
            request.form['city'],
            request.form['state'],
            request.form['zip'],
            request.form['pdid'],
            request.form['piid']
            ]
            db.insertPatient(data)
            return redirect('/view/2/patient') # Redirect to view
        if btnname == 'Update': # Update data
            data = [
            request.form['patid'],
            request.form['pdid'],
            request.form['piid'],
            request.form['state'],
            request.form['zip'],
            request.form['fname'],
            request.form['minit'],
            request.form['lname'],
            request.form['street'],
            request.form['city'],
            ]
            db.updatePatient(data)
            return redirect('/view/2/patient') # Redirect to view
        pass
    return render_template('patient_iu.html',activeclass=2,docid=docid,patid=patid,insid=insid,data=data)

@app.route('/appointmentiu',methods=('GET','POST'))
def appointmentiu():
    docid = sorted(db.getDoctorId())
    patid = sorted(db.getPatientId())
    facid = sorted(db.getColumn('facility','facid'))
    if request.method == 'POST':
        data = [
            request.form['docid'],
            request.form['patid'],
            request.form['facid'],
            request.form['appdatetime']
        ]
        db.insertMakesAppointment(data)
        return redirect('/view/2/patientappointment')
    return render_template('appointment_iu.html',activeclass=2,docid=docid,patid=patid,facid=facid)

@app.route('/q1')
def q1():
    return render_template('q1.html',activeclass=3)

@app.route('/q2')
def q2():
    phy = db.getPhysicianNames()
    return render_template('q2.html',activeclass=3,phy=phy)

@app.route('/q3')
def q3():
    fac = db.getFacilityNames()
    return render_template('q3.html',activeclass=3,fac=fac)

@app.route('/q4')
def q4():
    months = [['01',"January"], ['02',"February"], ['03',"March"], ['04',"April"], ['05',"May"], ['06',"June"], ['07',"July"], ['08',"August"], ['09',"September"], ['10',"October"], ['11',"November"], ['12',"December"]]
    return render_template('q4.html',activeclass=3,months=months)

@app.route('/q5')
def q5():
    return render_template('q5.html',activeclass=3)

@app.route('/iciu')
def iciu():
    return render_template('ic_iu.html',activeclass=2)

@app.route('/deletepatientappointment/<deleteno>')
def abc(deleteno):
    data = []
    tmp = db.getAppointment()
    for x in tmp:
        a = list(x)
        data.append(a)
    deletedata = data[int(deleteno)]
    db.deleteMakesAppointment(deletedata[0], deletedata[2], deletedata[4], deletedata[6])
    return redirect('/view/2/patientappointment')

@app.route('/manageappointment/<appno>',methods=('GET','POST'))
def manageappointment(appno):
    data = db.getAppointment()[int(appno)]
    if request.method == 'POST':
        cost = request.form['cost']
        newid = db.getMaxInvoiceId()+1
        newdata = [
            newid,
            data[0],
            data[2], # Patient ID
            data[4],
            data[6],
            cost
        ]
        db.insertInvoiceDetail(newdata)
        newdata = [
            newid,
            db.getInsOfPatient(data[2]),
            db.getDate(),
            cost
        ]
        db.insertInvoice(newdata)
        return redirect('/view/2/invoiceEverything')
    return render_template('complete_appointment.html',data=data,appno=appno)

@app.route('/view/<activeclass>/<what>',methods=('GET','POST'))
def view(activeclass,what):
    questions = ['q1','q2','q3','q4','q5']
    if what in questions:
        q = questions.index(what)+1
        if q == 1: # For a given day, a report of the revenue (patient charges recorded) by facility, with subtotals and a total.
            tmp = db.getAnswer(q,request.form['date'])
        if q == 2:
            tmp = db.getAnswer(q,request.form['date'],request.form['phy'])
        if q == 3:
            tmp = db.getAnswer(q,request.form['startdate'],request.form['enddate'],request.form['fac'])
        if q == 4:
            tmp = db.getAnswer(q,request.form['month'])
        if q == 5:
            tmp = db.getAnswer(q,request.form['startdate'],request.form['enddate'])
        heading = tmp[0]
        data = tmp[1]
        if q == 1:
            pass
    elif what == 'invoiceEverything':
        data = db.getEverythingInvoice()
        heading = db.getEverythingInvoiceHeading()
        pass
    elif what == 'patient':
        data = db.getPatient()
        heading = db.getPatientHeading()
        pass
    elif what == 'uniqueappointment':
        data = db.getUniqueAppointment()
        heading = db.getUniqueAppointmentHeading()
        pass
    elif what == 'patientappointment':
        data = []
        tmp = db.getAppointment()
        ctr = 0
        for x in tmp:
            a = list(x)
            a.append(f"<a href='/deletepatientappointment/{ctr}'>Delete</a>")
            a.append(f"<a href='/manageappointment/{ctr}'>Complete appointment</a>")
            data.append(a)
            ctr += 1
        heading = db.getAppointmentHeading()
        heading.append('Delete Appointment')
        heading.append('Complete Appointment')
        pass
    elif what == 'insurancecompanyinvoice':
        fullData = db.getICInvoice()
        # fullData : [['table heading','heading','data'], ['table heading','heading','data']]
        return render_template('double_view.html',activeclass=int(activeclass),fullData = fullData)
    elif what == 'insurancecompanyinvoicecustom':
        # fullData : [['table heading','heading','data'], ['table heading','heading','data']]
        if request.method == 'POST':
            fullData = db.getICInvoice(request.form['date'])
            return render_template('double_view.html',activeclass=int(activeclass),fullData = fullData)
    elif what == 'employee':
        data = db.employee()
        heading = db.employeeHeading()
    elif what == 'office':
        data = db.office()
        heading = db.officeHeading()
    elif what == 'outpatient_surgery':
        data = db.ops()
        heading = db.opsHeading()
    elif what == 'employeeassignment':
        data = db.employeeAssignments()
        heading = db.employeeAssignmentsHeading()
    else:
        data= db.getData(what)
        heading = db.tableHeading(what)
    return render_template('view.html',activeclass=int(activeclass),heading=heading,data=data)


if __name__ == "__main__":
    app.run(debug=True)