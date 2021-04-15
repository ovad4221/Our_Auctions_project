from secret_keys import SITE_SECRET_KEY
from werkzeug.security import check_password_hash


def check_token(token):
    return check_password_hash('pbkdf2:sha256:150000$' + token, SITE_SECRET_KEY)

print(
check_token('Gbimch77$a471f741437d48d728992c855204a8304ead06b8236d932fdd42bded9d0283c7'),
check_token('rFfXVUcC$78f3c1120eba4146c27dbf09ffc181f97005a5f677a5d73b35c427b63db2b326'),
check_token('4mFmmGBy$64bc720dfc0c97ed4528c650cc71a21678c67360de4c9fcf54324880da8496b1')
)