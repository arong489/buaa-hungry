import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { SwipeCell, Loading, Divider, Tag, Overlay, Icon, Tab, Tabs, Tabbar, TabbarItem, ActionBar, ActionBarIcon, ActionBarButton, DatetimePicker, TreeSelect, Stepper, Toast, Checkbox, CheckboxGroup, SubmitBar, ContactCard, Card, Dialog, AddressEdit, AddressList, Form, Field, CellGroup, Button, Uploader, DropdownItem, DropdownMenu, Picker, Popup, Empty, Image as VanImage } from 'vant'
import './common/css/base.less'
import axios from 'axios'

const app = createApp(App)
app.config.globalProperties.$axios = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/'
app.use(store).use(router).use(VanImage).use(SwipeCell).use(Loading).use(Divider).use(Tag).use(Icon).use(Tab).use(Overlay).use(Tabs).use(Tabbar).use(TabbarItem).use(DatetimePicker).use(ActionBar).use(ActionBarIcon).use(ActionBarButton).use(TreeSelect).use(Stepper).use(Toast).use(Checkbox).use(CheckboxGroup).use(SubmitBar).use(ContactCard).use(Card).use(Dialog).use(AddressEdit).use(Popup).use(Empty).use(AddressList).use(Form).use(Field).use(CellGroup).use(Button).use(Uploader).use(DropdownItem).use(DropdownMenu).use(Picker).mount('#app')
