from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from server.apps.core.models import CreatedAtMixin, UpdatedAtMixin, UUIDMixin
from server.apps.departments.managers import DepartmentManager


class Department(UUIDMixin, CreatedAtMixin, UpdatedAtMixin):
    """Модель подразделения."""

    name = models.CharField(
        verbose_name="название",
        max_length=200,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="родительское подразделение",
    )

    objects = DepartmentManager()

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'подразделения'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'name'],
                name='unique_department_name_in_parent'
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Проверка на цикл и ссылку на самого себя."""

        if self.parent and self.parent_id == self.id:
            raise ValidationError('Подразделение не может быть родителем самого себя.')

        if self.parent:
            ancestor = self.parent
            while ancestor:
                if ancestor == self:
                    raise ValidationError('Циклическая ссылка в структуре подразделений.')
                ancestor = ancestor.parent


class Employee(UUIDMixin, CreatedAtMixin, UpdatedAtMixin):
    """Модель сотрудника."""

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name="подразделение",
    )
    full_name = models.CharField(
        verbose_name="полное имя",
        max_length=200,
    )
    position = models.CharField(
        verbose_name="должность",
        max_length=200,
    )
    hired_at = models.DateField(
        verbose_name="дата найма",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name} — {self.position}"
    
    def clean(self):
        """Проверка на дату найма в будущем и отсутствие подразделения."""

        if self.hired_at and self.hired_at > timezone.now().date():
            raise ValidationError('Дата найма не может быть в будущем.')
        
        if not self.department:
            raise ValidationError('Сотрудник должен быть привязан к подразделению.')
