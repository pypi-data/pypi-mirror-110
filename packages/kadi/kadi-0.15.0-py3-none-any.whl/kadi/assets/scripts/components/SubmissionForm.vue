<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <form :action="action" :method="method" :enctype="enctype" @change="unsavedChanges = true" ref="form">
    <slot></slot>
  </form>
</template>

<script>
export default {
  data() {
    return {
      unsavedChanges: false,
    };
  },
  props: {
    selector: {
      type: String,
      default: '#submit',
    },
    action: {
      type: String,
      default: '',
    },
    method: {
      type: String,
      default: 'post',
    },
    enctype: {
      type: String,
      default: 'application/x-www-form-urlencoded',
    },
    checkDirty: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    beforeUnload(e) {
      // This way we can also deal with multiple forms on the same page.
      const isSubmitInput = window._lastClicked instanceof HTMLInputElement && window._lastClicked.type === 'submit';
      const withinOffset = (new Date().getTime() - window._lastClickedTime) < 100;

      if (this.unsavedChanges && !(isSubmitInput && withinOffset)) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
      return null;
    },
  },
  mounted() {
    const form = this.$refs.form;
    form.addEventListener('submit', () => form.querySelector(this.selector).disabled = true);
    form.addEventListener('click', (e) => {
      window._lastClicked = e.target;
      window._lastClickedTime = new Date().getTime();
    });

    if (this.checkDirty) {
      window.addEventListener('beforeunload', this.beforeUnload);
    }
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
