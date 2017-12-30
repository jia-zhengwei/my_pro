from django.core.files import File
from django.http import (JsonResponse)
from django.shortcuts import (render, redirect)
from pyexcel_xlsx import get_data
from sqlalchemy.orm import joinedload

from dbctrl.db_relation import *
from dbctrl.mysql_con import OperateDatabase
from info.data import DataOperation
from info.insert_database import (insert_process, insert_pfmea, insert_control, insert_special)

operation_database = OperateDatabase()


def get_document(request):
    if request.method == 'GET':
        pro_id = request.GET.get('pro_id', '')

        docs = []
        with operation_database.session_scope() as session:
            documents = session.query(Document).filter(Document.project_id == pro_id).all()
            for doc in documents:
                docment = {}
                docment['id'] = doc.id
                docment['filename'] = doc.filename
                docs.append(docment)
                print(docment)
            return JsonResponse(dict(docs=docs))


def show_project(request):

    data = {}
    with operation_database.session_scope() as session:
        user = session.query(User).filter(User.id == request.session['id']).first()
        print(user)
        groups = session.query(Group).filter(Group.company_id == user.company_id).all()
        projects = session.query(Project).options(joinedload(Project.groups), joinedload(Project.documents)). \
            filter(Project.company_id == user.company_id).all()
        data['projects'] = projects
        data['groups'] = groups
        return data


def project_list(request):
    with operation_database.session_scope() as session:
        data = show_project(request)
        return render(request, 'project/project_list.html', {'projects': data['projects'], \
                                                             'groups': data['groups']})


def add_project(request):
    if request.method == 'POST':
        pro_name = request.POST.get('pro_name')
        groups = request.POST.getlist('select2')
        descripe = request.POST.get('pro_descripe')
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session['user']['id']).first()
            company = session.query(Company).filter(Company.id == user.company_id).first()
            project = Project()
            project.pro_name = pro_name
            project.descripe = descripe
            if company:
                project.company_id = company.id
            for li in groups:
                group = session.query(Group).filter(Group.id == li).first()
                project.groups.append(group)
            session.add(project)
            return redirect('project:project_list')


def edit_project(request, pro_id):
    if request.method == 'GET':
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session['user']['id']).first()
            project = session.query(Project).filter(Project.id == pro_id).first()
            groups_all = session.query(Group).filter(Group.company_id == user.company_id).all()
            groups = session.query(Group).filter(Group.projects.any(Project.id == pro_id)).all()
            return render(request, 'project/project_edit.html',\
             {'project': project, 'groups': groups, 'groups_all': groups_all})
    else:
        with operation_database.session_scope() as session:
            groups = []
            user = session.query(User).filter(User.id == request.session['user']['id']).first()
            project = session.query(Project).filter(Project.id == pro_id).first()
            project.pro_name = request.POST.get('pro_name')
            project.descripe = request.POST.get('pro_descripe')
            for li in request.POST.getlist('select2'):
                group = session.query(Group).filter(Group.id == li).first()
                groups.append(group)
                project.groups = groups
            groups_all = session.query(Group).filter(Group.company_id == user.company_id).all()
            # groups = session.query(Group).filter(Group.projects.any(Project.id == pro_id)).all()
            return render(request, 'project/project_edit.html',\
             {'project': project, 'groups': project.groups, 'groups_all': groups_all})


def upload_file(request):
    if request.method == 'GET':
        data = show_project(request)
        return render(request, 'project/upload_file.html', {'projects': data['projects']})
    else:
        obj = request.FILES.get('file')
        file_type = request.POST.get('type', '')
        filename = File(obj).name
        desperation = DataOperation(get_data(obj))
        new_data = desperation.update_data()
        with operation_database.session_scope() as session:
            record = Record()
            user = session.query(User).filter(User.id == request.session['user']['id']).first()
            project = session.query(Project). \
                filter(Project.id == request.POST.get('select2')).first()
            document = Document()
            document.filename = filename
            document.descripe = request.POST.get('doc_descripe', '')
            if file_type == "control":
                record.descripe = '上传'+filename+'文件'
                user.records.append(record)
                document.records.append(record)
                insert_control(session, desperation.data_control(new_data))
            elif file_type == "process":
                record.descripe = '上传'+filename+'文件'
                user.records.append(record)
                document.records.append(record)
                project.processes.extend(insert_process(desperation.data_process(new_data)))
            elif file_type == "failure":
                record.descripe = '上传'+filename+'文件'
                user.records.append(record)
                document.records.append(record)
                insert_pfmea(session, desperation.data_failure(new_data))
            elif file_type == "special":
                record.descripe = '上传'+filename+'文件'
                user.records.append(record)
                document.records.append(record)
                insert_special(session, desperation.data_special(new_data))
            project.documents.append(document)
            return redirect('project:upload_file')



# def download_file(request, doc_id):
#     if request.method == 'GET':
#         print(doc_id)


def del_project(request, pro_id):
    if request.method == 'GET':
        with operation_database.session_scope() as session:
            project = session.query(Project).filter(Project.id == pro_id).first()
            session.delete(project)
            return redirect('project:project_list')

