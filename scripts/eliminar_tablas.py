import sqlite3

def eliminar_table(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nombre_tabla}'")
    tabla_existe = cursor.fetchone()
    if tabla_existe:
        cursor.execute(f"DROP TABLE {nombre_tabla}")
        print(f"La tabla '{nombre_tabla}' ha sido eliminada.")
    else:
        print(f"La tabla '{nombre_tabla}' no existe.")
    conexion.commit()
    conexion.close()

def run():
    eliminar_table('auth_user_groups')
    eliminar_table('auth_user_user_permissions')
    eliminar_table('auth_group_permissions')
    eliminar_table('auth_group')
    eliminar_table('auth_permission')
    eliminar_table('django_admin_log')
    eliminar_table('django_content_type')
    eliminar_table('django_migrations')
    eliminar_table('django_session')
    eliminar_table('Bodega')
    eliminar_table('DetalleBoleta')
    eliminar_table('Boleta')
    eliminar_table('Perfil')
    eliminar_table('Carrito')
    eliminar_table('Producto')
    eliminar_table('Categoria')
    eliminar_table('authtoken_token')
    eliminar_table('auth_user')

