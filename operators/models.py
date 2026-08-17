from django.contrib.auth.models import AbstractUser


class Operator(AbstractUser):
    """
    Usuário autenticável do NEXO NODE.

    Os campos específicos do universo NEXO serão adicionados
    nas próximas sprints.
    """

    def __str__(self):
        return self.username