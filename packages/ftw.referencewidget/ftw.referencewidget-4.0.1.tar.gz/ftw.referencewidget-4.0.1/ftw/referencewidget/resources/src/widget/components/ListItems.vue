<template>
  <ul class="list-group">
    <template v-for="item in items" :key="item.UID">
      <li
        class="list-group-item d-flex justify-content-between align-items-start"
      >
        <div
          :class="
            this.inputType == 'checkbox'
              ? 'form-check form-switch'
              : 'form-check'
          "
        >
          <input
            class="form-check-input me-1"
            :type="inputType"
            :value="{ title: item.title, url: item['@id'] }"
            v-model="selectedProxy"
            @change="checked"
            :disabled="isDisabled(item)"
            :role="this.inputType == 'checkbox' ? 'switch' : ''"
          />
          <label
            :class="
              isDisabled(item) && isTraversable(item) ? '' : 'form-check-label'
            "
          >
            <ResolveIcon :item="item" :iconMapping="iconMapping" />
            <a
              v-if="item.is_folderish && isTraversable(item)"
              @click.prevent.stop="fetchData(item['@id'])"
              :href="item['@id']"
              class="list-group-item-action"
              >{{ item.title }}
              <span class="portal-type">({{ item["portal_type"] }})</span>
            </a>
            <span v-else>
              {{ item.title }}
              <span :class="`state-${item['review_state']}`"
                >{{ workflowTitleMapping[item["review_state"]] }}
                <span class="portal-type">({{ item["portal_type"] }})</span>
              </span>
            </span>
          </label>
        </div>
        <span class="badge bg-primary rounded-pill" v-if="item['review_state']">
          <span :class="`state-${item['review_state']}`">{{
            workflowTitleMapping[item["review_state"]]
          }}</span>
        </span>
      </li>
    </template>
  </ul>
</template>
<script>
import ResolveIcon from "./ResolveIcon.vue";
export default {
  components: {
    ResolveIcon,
  },
  data() {
    return {
      selected: [],
    };
  },
  props: {
    items: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    selectedItems: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    inputType: {
      type: String,
      required: true,
      default: () => {
        return "checkbox";
      },
    },
    selectableTypes: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    traversableTypes: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    iconMapping: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
    workflowTitleMapping: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
    fetchData: {
      type: Function,
      required: true,
      default: () => {
        return null;
      },
    },
  },
  mounted() {
    this.selected = this.selectedItems;
  },
  methods: {
    checked() {
      this.$emit("checked", this.selected);
    },
    isDisabled(item) {
      return this.selectableTypes.indexOf(item.portal_type) == -1;
    },
    isTraversable(item) {
      return this.traversableTypes.indexOf(item.portal_type) != -1;
    },
  },
  computed: {
    selectedProxy: {
      get() {
        if (this.inputType == "checkbox") {
          return this.selected;
        } else {
          return this.selected[0];
        }
      },
      set(value) {
        if (this.inputType == "checkbox") {
          this.selected = value;
        } else {
          this.selected = [value];
        }
      },
    },
  },
};
</script>
