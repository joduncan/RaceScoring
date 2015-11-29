# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    The main grid for towerrunning usa's scoring system
    """

    categories = [ 'Open' , 
                   '5-9' , 
                   '10-19' , 
                   '20-29' ,
                   '30-39' , 
                   '40-49' , 
                   '50-59' , 
                   '60-69' , 
                   '70-79' , 
                   '80-89' , 
                   '90-99' ] 


    if session.chosenSex==None:
      chosenSex = 'M'
    if session.chosenCategory==None:
      session.chosenCategory = 'Open'
    
    f1 = Field('sex', requires=IS_IN_SET(('M','F'),zero=None),default=session.chosenSex)
    f2 = Field('category', requires=IS_IN_SET(categories,zero=None),default=session.chosenCategory)
    
    form = SQLFORM.factory(f1,
                           f2 ,
                           Field('name') )
    ds = db.sheets
    fields = [ ds.ranking , ds.name , ds.age, ds.points, ds.results ]
    
    if form.process(keepvalues=True).accepted:
      session.chosenSex = form.vars.sex
      session.chosenCategory = form.vars.category 
      session.namesearch = form.vars.name
     

    q = (db.sheets.sex==session.chosenSex) & (db.sheets.category == session.chosenCategory)
    if session.namesearch <> None:
      q = q & (db.sheets.name.like( '%' + session.namesearch + '%' ))

    print q 

    grid = SQLFORM.grid( q , fields = fields , search_widget = None )
    return dict(options=form,results=grid)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


