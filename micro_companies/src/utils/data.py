from micro_companies.src.models.models import *

def generateSectors():
    if not has_records(CompanySector):
        sector1 = CompanySector(name = 'Tecnología')
        sector2 = CompanySector(name = 'Salud y Ciencias de la Vida')
        sector3 = CompanySector(name = 'Energía y Recursos Naturales')
        sector4 = CompanySector(name = 'Finanzas y Banca')
        sector5 = CompanySector(name = 'Manufactura')
        sector6 = CompanySector(name = 'Comercio Minorista y Consumo')
        sector7 = CompanySector(name = 'Educación')
        sector8 = CompanySector(name = 'Entretenimiento y Medios')
        sector9 = CompanySector(name = 'Transporte y Logística')
        sector10 = CompanySector(name = 'Servicios Profesionales')

        db.session.add(sector1)
        db.session.add(sector2)
        db.session.add(sector3)
        db.session.add(sector4)
        db.session.add(sector5)
        db.session.add(sector6)
        db.session.add(sector7)
        db.session.add(sector8)
        db.session.add(sector9)
        db.session.add(sector10)

        db.session.commit()

def generateTypes():
    if not has_records(CompanyType):
        sector1 = CompanySector.query.get(1)
        sector2 = CompanySector.query.get(2)
        sector3 = CompanySector.query.get(3)
        sector4 = CompanySector.query.get(4)
        sector5 = CompanySector.query.get(5)
        sector6 = CompanySector.query.get(6)
        sector7 = CompanySector.query.get(7)
        sector8 = CompanySector.query.get(8)
        sector9 = CompanySector.query.get(9)
        sector10 = CompanySector.query.get(10)

        tipo1 = CompanyType(name = 'Empresas de software',  sector_id=sector1.id)
        tipo2 = CompanyType(name = 'Empresas de hardware',  sector_id=sector1.id)
        tipo3 = CompanyType(name = 'Empresas de telecomunicaciones',  sector_id=sector1.id)

        tipo4 = CompanyType(name = 'Farmacéuticas',  sector_id=sector2.id)
        tipo5 = CompanyType(name = 'Hospitales y sistemas de atención médica',  sector_id=sector2.id)
        tipo6 = CompanyType(name = 'Empresas de dispositivos médicos',  sector_id=sector2.id)

        tipo7 = CompanyType(name = 'Compañías petroleras y gasísticas',  sector_id=sector3.id)
        tipo8 = CompanyType(name = 'Empresas de energía renovable',  sector_id=sector3.id)
        tipo9 = CompanyType(name = 'Minería',  sector_id=sector3.id)

        tipo10 = CompanyType(name = 'Bancos comerciales',  sector_id=sector4.id)
        tipo11 = CompanyType(name = 'Empresas de gestión de activos',  sector_id=sector4.id)
        tipo12 = CompanyType(name = 'Aseguradoras',  sector_id=sector4.id)

        tipo13 = CompanyType(name = 'Automotrices',  sector_id=sector5.id)
        tipo14 = CompanyType(name = 'Empresas de productos electrónicos',  sector_id=sector5.id)
        tipo15 = CompanyType(name = 'Fabricantes de alimentos y bebidas',  sector_id=sector5.id)

        tipo16 = CompanyType(name = 'Tiendas minoristas',  sector_id=sector6.id)
        tipo17 = CompanyType(name = 'Empresas de alimentos rápidos',  sector_id=sector6.id)
        tipo18 = CompanyType(name = 'Empresas de moda',  sector_id=sector6.id)

        tipo19 = CompanyType(name = 'Universidades e instituciones educativas',  sector_id=sector7.id)
        tipo20 = CompanyType(name = 'Plataformas de aprendizaje en línea',  sector_id=sector7.id)
        tipo21 = CompanyType(name = 'Editoriales educativas',  sector_id=sector7.id)

        tipo22 = CompanyType(name = 'Estudios de cine y televisión',  sector_id=sector8.id)
        tipo23 = CompanyType(name = 'Plataformas de transmisión en línea',  sector_id=sector8.id)
        tipo24 = CompanyType(name = 'Editoriales',  sector_id=sector8.id)

        tipo25 = CompanyType(name = 'Aerolíneas',  sector_id=sector9.id)
        tipo26 = CompanyType(name = 'Compañías de logística y envío',  sector_id=sector9.id)
        tipo27 = CompanyType(name = 'Fabricantes de vehículos',  sector_id=sector9.id)

        tipo28 = CompanyType(name = 'Empresas de consultoría',  sector_id=sector10.id)
        tipo29 = CompanyType(name = 'Despachos de abogados',  sector_id=sector10.id)
        tipo30 = CompanyType(name = 'Agencias de publicidad',  sector_id=sector10.id)


        db.session.add(tipo1)
        db.session.add(tipo2)
        db.session.add(tipo3)
        db.session.add(tipo4)
        db.session.add(tipo5)
        db.session.add(tipo6)
        db.session.add(tipo7)
        db.session.add(tipo8)
        db.session.add(tipo9)
        db.session.add(tipo10)

        db.session.add(tipo11)
        db.session.add(tipo12)
        db.session.add(tipo13)
        db.session.add(tipo14)
        db.session.add(tipo15)
        db.session.add(tipo16)
        db.session.add(tipo17)
        db.session.add(tipo18)
        db.session.add(tipo19)
        db.session.add(tipo20)

        db.session.add(tipo21)
        db.session.add(tipo22)
        db.session.add(tipo23)
        db.session.add(tipo24)
        db.session.add(tipo25)
        db.session.add(tipo26)
        db.session.add(tipo27)
        db.session.add(tipo28)
        db.session.add(tipo29)
        db.session.add(tipo30)

        db.session.commit()


def init_data():
    try:
        db.create_all()
        generateSectors()
        generateTypes()

    except Exception as e:
        print("already loaded",str(e))


def has_records(model):
    return db.session.query(model).count() > 0