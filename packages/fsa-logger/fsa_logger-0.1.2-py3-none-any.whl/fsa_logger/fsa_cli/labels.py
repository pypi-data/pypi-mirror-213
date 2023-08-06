from ..config.config import AppConfig

config = AppConfig()
index = 1 if config.language == 'ES' else 0
MENU_OPTION_CONFIG = [
    'Config',
    'Configurar',
][index]
MENU_OPTION_EXIT = [
    'Exit',
    'Salir',
][index]
MENU_OPTION_BACK = [
    'Back',
    'Atrás',
][index]

MENU_OPTION_SENSORS = [
    'Sensors',
    'Sensores',
][index]
MENU_OPTION_COLLECT_SENSORS = [
    'Collect available sensors',
    'Conectar sensores en rango',
][index]
MENU_OPTION_SHOW_SENSORS = [
    'Show sensors',
    'Ver sensores',
][index]
MENU_OPTION_EDIT_SENSORS = [
    'Edit sensors',
    'Editar sensores',
][index]
MENU_OPTION_CONFIG_SENSORS = [
    'Config sensors',
    'Configurar sensores',
][index]
MENU_OPTION_SEARCH_SENSORS = [
    'Search sensors',
    'Buscar sensores',
][index]
MENU_OPTION_CONNECT_SENSORS = [
    'Connect sensors',
    'Conectar sensores',
][index]
MENU_OPTION_DISCONNECT_SENSORS = [
    'Disconnect sensors',
    'Desconectar sensores',
][index]
MENU_OPTION_TEST_SENSORS = [
    'Test sensors',
    'Test sensores',
][index]

MENU_OPTION_SESSIONS = [
    'Sessions',
    'Sesiones',
][index]
MENU_OPTION_LIST_SESSIONS = [
    'List sessions',
    'Ver sesiones',
][index]
MENU_OPTION_SELECT_SESSION = [
    'Select session',
    'Seleccionar sesión',
][index]
MENU_OPTION_QUICK_CAPTURE = [
    'Quick capture session',
    'Sesión de captura rápida',
][index]
MENU_OPTION_CREATE_SESSION = [
    'Create session',
    'Crear sesión',
][index]
MENU_OPTION_EDIT_SESSION = [
    'Edit session',
    'Modificar sesión',
][index]
MENU_OPTION_DELETE_SESSIONS = [
    'Delete sessions',
    'Eliminar sesiones',
][index]
MENU_OPTION_MERGE_SESSIONS = [
    'Merge sessions',
    'Unir sesiones',
][index]
MENU_OPTION_RESTORE_SESSION = [
    'Restore session',
    'Restaurar sesión',
][index]
MENU_OPTION_CLEAR_SESSIONS_DATA = [
    'Clear sessions data',
    'Limpiar datos de sesiones',
][index]

MENU_OPTION_SESSION = [
    'Session',
    'Sesión',
][index]
MENU_OPTION_DELETE_SESSION = [
    'Delete current session',
    'Eliminar sesión actual',
][index]
MENU_OPTION_CLEAR_SESSION_DATA = [
    'Clear current session data',
    'Limpiar datos de la sesión actual',
][index]
MENU_OPTION_START_SESSION_CAPTURE = [
    'Start capture',
    'Iniciar captura',
][index]
MENU_OPTION_EXPORT_SESSION_DATA = [
    'Export session data',
    'Exportar datos de la sesión',
][index]
MENU_OPTION_SHOW_SESSION_DATA = [
    'Show session data',
    'Mostrar los datos de la sesión',
][index]
MENU_OPTION_ANALYZE_SESSION_DATA = [
    'Analyze session',
    'Analizar sesión',
][index]
