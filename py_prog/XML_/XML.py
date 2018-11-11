import xml.etree.ElementTree as ET
tree = ET.parse('xml_test.xml')
root = tree.getroot()
print(root.tag)
for students in root:
    print (students.tag)
    print(students.attrib)
    if (len(students))!=0:
        for subjects in students:
            print(subjects.attrib['name']+ ':'+ subjects.text)

#student= ET.SubElement(root, 'student', {'name':'Doctor', 'surname': 'Who'})
#tree.write('xml_test.xml')

def add_smth(root):
    name=input()
    surname=input()
    student= ET.SubElement(root, 'student', {'name':name, 'surname': surname})
    print('Grade of proga:')
    proga=input()
    subject_p = ET.SubElement(student, 'subject', {'name': "Proga"})
    subject_p.text = proga
    print('Grade of matan:')
    matan=input()
    subject_p = ET.SubElement(student, 'subject', {'name': "Matan"})
    subject_p.text = matan
    print('Grade of eng:')
    eng=input()
    subject_p = ET.SubElement(student, 'subject', {'name': "Eng"})
    subject_p.text = eng
    print('Grade of linal:')
    linal=input()
    subject_p = ET.SubElement(student, 'subject', {'name': "Linal"})
    subject_p.text = linal
    tree.write('xml_test.xml')
    print('ok')

add_smth(root)


