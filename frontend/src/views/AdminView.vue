<template>
  <v-container fluid class="pa-4">
    <h1 class="text-h5 font-weight-bold mb-4">Administration</h1>

    <v-tabs v-model="activeTab" color="primary" show-arrows class="mb-1">
      <v-tab value="groups">Groups</v-tab>
      <v-tab value="divisions">Divisions</v-tab>
      <v-tab value="locations">Locations</v-tab>
      <v-tab value="employees">Employees</v-tab>
      <v-tab value="payroll">Payroll</v-tab>
      <v-tab value="holidays">Holidays</v-tab>
      <v-tab value="templates">Schedule Templates</v-tab>
    </v-tabs>
    <v-divider class="mb-4" />

    <v-tabs-window v-model="activeTab">

      <!-- ── GROUPS ──────────────────────────────────────── -->
      <v-tabs-window-item value="groups">
        <EntityPanel
          title="Groups"
          :items="groups || []"
          :loading="groupsLoading"
          :headers="[{ key: 'id', label: 'ID' }, { key: 'group_name', label: 'Name' }]"
          @new="openCreate('groups')"
          @edit="openEdit('groups', $event)"
          @delete="confirmDelete('groups', $event)"
        />
      </v-tabs-window-item>

      <!-- ── DIVISIONS ──────────────────────────────────── -->
      <v-tabs-window-item value="divisions">
        <EntityPanel
          title="Divisions"
          :items="divisions || []"
          :loading="divisionsLoading"
          :headers="[{ key: 'id', label: 'ID' }, { key: 'division_name', label: 'Name' }]"
          @new="openCreate('divisions')"
          @edit="openEdit('divisions', $event)"
          @delete="confirmDelete('divisions', $event)"
        />
      </v-tabs-window-item>

      <!-- ── LOCATIONS ──────────────────────────────────── -->
      <v-tabs-window-item value="locations">
        <EntityPanel
          title="Locations"
          :items="locations || []"
          :loading="locationsLoading"
          :headers="[{ key: 'id', label: 'ID' }, { key: 'location_name', label: 'Name' }]"
          @new="openCreate('locations')"
          @edit="openEdit('locations', $event)"
          @delete="confirmDelete('locations', $event)"
        />
      </v-tabs-window-item>

      <!-- ── EMPLOYEES ──────────────────────────────────── -->
      <v-tabs-window-item value="employees">
        <EntityPanel
          title="Employees"
          :items="employees || []"
          :loading="employeesLoading"
          :headers="[
            { key: 'id', label: 'ID' },
            { key: '_name', label: 'Name' },
            { key: '_division', label: 'Division' },
            { key: '_group', label: 'Group' },
            { key: '_location', label: 'Location' },
            { key: 'start_date', label: 'Start' },
          ]"
          :cell-formatter="employeeCellFormatter"
          @new="openCreate('employees')"
          @edit="openEdit('employees', $event)"
          @delete="confirmDelete('employees', $event)"
        />
      </v-tabs-window-item>

      <!-- ── PAYROLL ─────────────────────────────────────── -->
      <v-tabs-window-item value="payroll">
        <EntityPanel
          title="Payroll Info"
          :items="payrollInfos || []"
          :loading="payrollLoading"
          :headers="[
            { key: 'id', label: 'ID' },
            { key: 'payroll_year', label: 'Year' },
            { key: 'payroll_start', label: 'Start Date' },
            { key: 'payroll_frequency', label: 'Frequency' },
            { key: 'week_start_day', label: 'Week Starts' },
          ]"
          @new="openCreate('payroll')"
          @edit="openEdit('payroll', $event)"
          @delete="confirmDelete('payroll', $event)"
        />
      </v-tabs-window-item>

      <!-- ── HOLIDAYS ────────────────────────────────────── -->
      <v-tabs-window-item value="holidays">
        <EntityPanel
          title="Holidays"
          :items="holidays || []"
          :loading="holidaysLoading"
          :headers="[
            { key: 'id', label: 'ID' },
            { key: 'holiday_name', label: 'Name' },
            { key: 'rule_type', label: 'Rule' },
            { key: '_rule_detail', label: 'Detail' },
            { key: 'observed_rule', label: 'Observed' },
          ]"
          :cell-formatter="holidayCellFormatter"
          @new="openCreate('holidays')"
          @edit="openEdit('holidays', $event)"
          @delete="confirmDelete('holidays', $event)"
        />
      </v-tabs-window-item>

      <!-- ── SCHEDULE TEMPLATES ─────────────────────────── -->
      <v-tabs-window-item value="templates">
        <EntityPanel
          title="Schedule Templates"
          :items="templates || []"
          :loading="templatesLoading"
          :headers="[
            { key: 'id', label: 'ID' },
            { key: '_employee', label: 'Employee' },
            { key: '_day', label: 'Day' },
            { key: 'start_time', label: 'Start' },
            { key: 'end_time', label: 'End' },
            { key: '_location', label: 'Location' },
          ]"
          :cell-formatter="templateCellFormatter"
          @new="openCreate('templates')"
          @edit="openEdit('templates', $event)"
          @delete="confirmDelete('templates', $event)"
        />
      </v-tabs-window-item>

    </v-tabs-window>

    <!-- ── CREATE / EDIT DIALOG ──────────────────────────── -->
    <AdminFormDialog
      :open="dialog.open"
      :title="dialog.title"
      :saving="isSaving"
      :max-width="dialog.entity === 'employees' || dialog.entity === 'templates' ? 680 : 560"
      @cancel="closeDialog"
      @save="triggerFormSubmit"
    >
      <SimpleNameForm
        v-if="dialog.entity === 'groups'"
        ref="formRef"
        :model-value="dialog.item"
        field-label="Group Name"
        field-key="group_name"
        @submit="onFormSubmit"
      />
      <SimpleNameForm
        v-else-if="dialog.entity === 'divisions'"
        ref="formRef"
        :model-value="dialog.item"
        field-label="Division Name"
        field-key="division_name"
        @submit="onFormSubmit"
      />
      <SimpleNameForm
        v-else-if="dialog.entity === 'locations'"
        ref="formRef"
        :model-value="dialog.item"
        field-label="Location Name"
        field-key="location_name"
        @submit="onFormSubmit"
      />
      <EmployeeForm
        v-else-if="dialog.entity === 'employees'"
        ref="formRef"
        :model-value="dialog.item"
        @submit="onFormSubmit"
      />
      <PayrollInfoForm
        v-else-if="dialog.entity === 'payroll'"
        ref="formRef"
        :model-value="dialog.item"
        @submit="onFormSubmit"
      />
      <HolidayForm
        v-else-if="dialog.entity === 'holidays'"
        ref="formRef"
        :model-value="dialog.item"
        @submit="onFormSubmit"
      />
      <ScheduleTemplateForm
        v-else-if="dialog.entity === 'templates'"
        ref="formRef"
        :model-value="dialog.item"
        @submit="onFormSubmit"
      />
    </AdminFormDialog>

    <!-- ── DELETE CONFIRM DIALOG ─────────────────────────── -->
    <v-dialog v-model="deleteDialog.open" max-width="400" persistent>
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete
          <strong>{{ deleteDialog.label }}</strong>? This cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog.open = false">Cancel</v-btn>
          <v-btn
            color="error"
            variant="flat"
            :loading="isDeleting"
            @click="executeDelete"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

import AdminFormDialog from "@/components/admin/AdminFormDialog.vue";
import EntityPanel from "@/components/admin/EntityPanel.vue";
import SimpleNameForm from "@/components/admin/forms/SimpleNameForm.vue";
import EmployeeForm from "@/components/admin/forms/EmployeeForm.vue";
import PayrollInfoForm from "@/components/admin/forms/PayrollInfoForm.vue";
import HolidayForm from "@/components/admin/forms/HolidayForm.vue";
import ScheduleTemplateForm from "@/components/admin/forms/ScheduleTemplateForm.vue";

import { useGroups } from "@/composables/useGroups.js";
import { useDivisions } from "@/composables/useDivisions.js";
import { useLocations } from "@/composables/useLocations.js";
import { useEmployees } from "@/composables/useEmployees.js";
import { usePayrollInfos } from "@/composables/usePayrollInfos.js";
import { useHolidays } from "@/composables/useHolidays.js";
import { useScheduleTemplates } from "@/composables/useScheduleTemplates.js";

const activeTab = ref("groups");
const formRef = ref(null);

// ── Data ──────────────────────────────────────────────────
const {
  data: groups,
  isLoading: groupsLoading,
  createMutation: createGroup,
  updateMutation: updateGroup,
  deleteMutation: deleteGroup,
} = useGroups();

const {
  data: divisions,
  isLoading: divisionsLoading,
  createMutation: createDivision,
  updateMutation: updateDivision,
  deleteMutation: deleteDivision,
} = useDivisions();

const {
  data: locations,
  isLoading: locationsLoading,
  createMutation: createLocation,
  updateMutation: updateLocation,
  deleteMutation: deleteLocation,
} = useLocations();

const {
  data: employees,
  isLoading: employeesLoading,
  createMutation: createEmployee,
  updateMutation: updateEmployee,
  deleteMutation: deleteEmployee,
} = useEmployees();

const {
  data: payrollInfos,
  isLoading: payrollLoading,
  createMutation: createPayroll,
  updateMutation: updatePayroll,
  deleteMutation: deletePayroll,
} = usePayrollInfos();

const {
  data: holidays,
  isLoading: holidaysLoading,
  createMutation: createHoliday,
  updateMutation: updateHoliday,
  deleteMutation: deleteHoliday,
} = useHolidays();

const templatesEmployeeId = ref(null);
const {
  data: templates,
  isLoading: templatesLoading,
  createMutation: createTemplate,
  updateMutation: updateTemplate,
  deleteMutation: deleteTemplate,
} = useScheduleTemplates(templatesEmployeeId);

// ── Dialog state ─────────────────────────────────────────
const dialog = ref({ open: false, entity: null, item: null, title: "" });
const deleteDialog = ref({ open: false, entity: null, item: null, label: "" });

function openCreate(entity) {
  dialog.value = { open: true, entity, item: null, title: createTitle(entity) };
}

function openEdit(entity, item) {
  dialog.value = { open: true, entity, item, title: editTitle(entity, item) };
}

function closeDialog() {
  dialog.value = { open: false, entity: null, item: null, title: "" };
}

function confirmDelete(entity, item) {
  deleteDialog.value = {
    open: true,
    entity,
    item,
    label: deleteLabel(entity, item),
  };
}

function triggerFormSubmit() {
  formRef.value?.submit();
}

// ── Mutation dispatch ─────────────────────────────────────
const MUTATIONS = computed(() => ({
  groups: { create: createGroup, update: updateGroup, delete: deleteGroup },
  divisions: {
    create: createDivision,
    update: updateDivision,
    delete: deleteDivision,
  },
  locations: {
    create: createLocation,
    update: updateLocation,
    delete: deleteLocation,
  },
  employees: {
    create: createEmployee,
    update: updateEmployee,
    delete: deleteEmployee,
  },
  payroll: { create: createPayroll, update: updatePayroll, delete: deletePayroll },
  holidays: {
    create: createHoliday,
    update: updateHoliday,
    delete: deleteHoliday,
  },
  templates: {
    create: createTemplate,
    update: updateTemplate,
    delete: deleteTemplate,
  },
}));

const isSaving = computed(() => {
  const m = MUTATIONS.value[dialog.value.entity];
  return (
    m?.create?.isPending.value || m?.update?.isPending.value || false
  );
});

const isDeleting = computed(() => {
  const m = MUTATIONS.value[deleteDialog.value.entity];
  return m?.delete?.isPending.value || false;
});

function onFormSubmit(values) {
  const { entity, item } = dialog.value;
  const m = MUTATIONS.value[entity];
  if (item) {
    m.update.mutate({ id: item.id, ...values }, { onSuccess: closeDialog });
  } else {
    m.create.mutate(values, { onSuccess: closeDialog });
  }
}

function executeDelete() {
  const { entity, item } = deleteDialog.value;
  const m = MUTATIONS.value[entity];
  m.delete.mutate(item.id, {
    onSuccess: () => {
      deleteDialog.value.open = false;
    },
  });
}

// ── Helpers ───────────────────────────────────────────────
const WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const MONTH_NAMES = [
  "Jan","Feb","Mar","Apr","May","Jun",
  "Jul","Aug","Sep","Oct","Nov","Dec",
];

function createTitle(entity) {
  const map = {
    groups: "New Group",
    divisions: "New Division",
    locations: "New Location",
    employees: "New Employee",
    payroll: "New Payroll Info",
    holidays: "New Holiday",
    templates: "New Schedule Template",
  };
  return map[entity] || "New";
}

function editTitle(entity, item) {
  const map = {
    groups: `Edit Group: ${item.group_name}`,
    divisions: `Edit Division: ${item.division_name}`,
    locations: `Edit Location: ${item.location_name}`,
    employees: `Edit Employee: ${item.first_name} ${item.last_name}`,
    payroll: `Edit Payroll: ${item.payroll_year}`,
    holidays: `Edit Holiday: ${item.holiday_name}`,
    templates: `Edit Template`,
  };
  return map[entity] || "Edit";
}

function deleteLabel(entity, item) {
  const map = {
    groups: item.group_name,
    divisions: item.division_name,
    locations: item.location_name,
    employees: `${item.first_name} ${item.last_name}`,
    payroll: `payroll info for ${item.payroll_year}`,
    holidays: item.holiday_name,
    templates: `template for ${item.employee?.first_name} ${item.employee?.last_name}`,
  };
  return map[entity] || "this item";
}

function employeeCellFormatter(key, item) {
  if (key === "_name") return `${item.last_name}, ${item.first_name}`;
  if (key === "_division") return item.division?.division_name ?? "—";
  if (key === "_group") return item.group?.group_name ?? "—";
  if (key === "_location") return item.location?.location_name ?? "—";
  return null;
}

function holidayCellFormatter(key, item) {
  if (key !== "_rule_detail") return null;
  if (item.rule_type === "fixed_date") {
    return `${MONTH_NAMES[(item.month ?? 1) - 1]} ${item.day}`;
  }
  if (item.rule_type === "nth_weekday") {
    return `${item.week}${ordinal(item.week)} ${WEEKDAY_NAMES[item.weekday ?? 0]} of ${MONTH_NAMES[(item.month ?? 1) - 1]}`;
  }
  if (item.rule_type === "last_weekday") {
    return `Last ${WEEKDAY_NAMES[item.weekday ?? 0]} of ${MONTH_NAMES[(item.month ?? 1) - 1]}`;
  }
  return "—";
}

function templateCellFormatter(key, item) {
  if (key === "_employee")
    return `${item.employee?.last_name}, ${item.employee?.first_name}`;
  if (key === "_day") return WEEKDAY_NAMES[item.day_of_week] ?? "—";
  if (key === "_location") return item.location?.location_name ?? "—";
  return null;
}

function ordinal(n) {
  if (n === 1) return "st";
  if (n === 2) return "nd";
  if (n === 3) return "rd";
  return "th";
}
</script>
