<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  schedule: {
    type: Object,
    default: () => ({
      employee: null,
      day_of_week: "",
      floor: "",
    }),
  },
  employees: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(["update:modelValue", "save-schedule"]);

const formData = ref({...props.schedule});

watch(
    () => props.schedule,
    (newVal) => {
      formData.value = {...newVal};
    },
    { immediate: true, deep: true },
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("save-schedule", {...formData.value, floor: Number(formData.value.floor)});
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>
        {{ schedule?.id ? "Редактировать расписание" : "Добавить расписание" }}
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.employee"
              :items="employees"
              item-title="full_name"
              item-value="id"
              label="Сотрудник"
              required/>
          <v-select
              v-model="formData.day_of_week"
              :items="[
              { text: 'Понедельник', value: 'mon' },
              { text: 'Вторник', value: 'tue' },
              { text: 'Среда', value: 'wed' },
              { text: 'Четверг', value: 'thu' },
              { text: 'Пятница', value: 'fri' },
              { text: 'Суббота', value: 'sat' },
              { text: 'Воскресенье', value: 'sun' },
            ]"
              item-title="text"
              item-value="value"
              label="День недели"
              required
          />
          <v-text-field
              v-model="formData.floor"
              label="Этаж"
              type="number"
              min="1"
              max="5"
              required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
