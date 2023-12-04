import {
    createStore
} from 'vuex'

export default createStore({
    state: {
        cartList: [], // 购物车数据
        orderList: [], // 生产订单数据
        edit: true, // 编辑的展示
        orderLists: [], // 新订单页面传入订单页面的数据
        userAddress: [{
            id: 1001,
            name: '玛卡巴卡',
            tel: '66666666666',
            school: '沙河校区',
            dorm: '大运村学生公寓',
            addressDetail: '大运村',
            isDefault: true,
            areaCode: '110101'
        }]
    },
    mutations: {
        ADDCART(state, value) { // 添加购物车
            state.cartList = value
        },
        PAY(state, value) { // 结算按钮
            state.orderList = value
        },
        DELETE(state, value) { // 删除按钮
            state.cartList = value
        },
        EDIT(state, value) { // 编辑按钮
            if (value === 'delete') {
                state.edit = true
            } else {
                state.edit = !state.edit
            }
        },
        UPORDERLIST(state) {
            state.orderLists = state.orderLists.concat(state.orderList)
        },
        // 增加地址
        ADDADDRESS(state, value) {
            state.userAddress.map((item) => {
                if (value.isDefault) {
                    item.isDefault = false
                }
            })
            state.userAddress.push(value);
        },
        // 编辑地址
        CHANGEADDRESS(state, value) {
            state.userAddress = state.userAddress.map((item) => {
                if (value.isDefault) {
                    item.isDefault = false
                }
                return value.id === item.id ? value : item
            })
        },
        // 删除地址
        DELECTADDRESS(state, value) {
            state.userAddress = state.userAddress.filter((item) => {
                return !(item.id === value.id)
            })
            if (value.isDefault && state.userAddress.length) {
                state.userAddress[0].isDefault = true
            }
        }
    },
    actions: {}

})