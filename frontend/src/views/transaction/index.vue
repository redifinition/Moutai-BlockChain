<!--
 * @Description: 
 * @Author: lyq
 * @Date: 2021-11-19 15:21:54
 * @LastEditTime: 2024-04-02 14:48:08
 * @LastEditors: lyq
-->
<template>
  <div class="app-container">
    <el-form
      :model="form"
      ref="form"
      :rules="rules"
      label-width="120px"
      style="width: 50%"
    >
      <el-form-item label="交易类型">
        <el-radio-group v-model="form.type" @change="onChangeType('form')">
          <el-radio label="production">生产交易</el-radio>
          <el-radio label="logistics">物流交易</el-radio>
          <el-radio label="sale">销售交易</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- 生产交易的表单项 -->
      <template v-if="form.type === 'production'">
        <el-form-item
          label="产品ID"
          prop="product_id"
          :rules="[
            { required: true, message: '产品ID不能为空' },
            { type: 'number', message: '产品ID必须为数字值' },
          ]"
        >
          <el-input v-model.number="form.product_id"></el-input>
        </el-form-item>
        <el-form-item
          label="批次号"
          prop="batch_number"
          :rules="[
            { required: true, message: '批次号不能为空' },
            { type: 'number', message: '批次号必须为数字值' },
          ]"
        >
          <el-input v-model.number="form.batch_number"></el-input>
        </el-form-item>
        <el-form-item
          label="生产日期"
          prop="production_date"
          :rules="[{ required: true, message: '生产日期不能为空' }]"
        >
          <el-date-picker
            v-model="form.production_date"
            type="date"
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item
          label="工厂"
          prop="factory"
          :rules="[{ required: true, message: '工厂不能为空' }]"
        >
          <el-input v-model="form.factory"></el-input>
        </el-form-item>
        <el-form-item
          label="原料产地"
          prop="origin_place"
          :rules="[{ required: true, message: '原料产地不能为空' }]"
        >
          <el-input v-model="form.origin_place"></el-input>
        </el-form-item>
      </template>
      <!-- 物流交易的表单项 -->
      <template v-if="form.type === 'logistics'">
        <el-form-item label="产品ID" prop="product_id"
        :rules="[
            { required: true, message: '产品ID不能为空' },
            { type: 'number', message: '产品ID必须为数字值' },
          ]">
          <el-input v-model.number="form.product_id"></el-input>
        </el-form-item>
        <el-form-item label="发货地址" prop="from_address"
        :rules="[
            { required: true, message: '发货地址不能为空' },
          ]">
          <el-input v-model="form.from_address"></el-input>
        </el-form-item>
        <el-form-item label="收货地址" prop="to_address"
        :rules="[
            { required: true, message: '收货地址不能为空' },,
          ]">
          <el-input v-model="form.to_address"></el-input>
        </el-form-item>
        <el-form-item label="运输公司" prop="carrier"
        :rules="[
            { required: true, message: '运输公司不能为空' },,
          ]">
          <el-input v-model="form.carrier"></el-input>
        </el-form-item>
        <el-form-item label="运单号" prop="tracking_number"
        :rules="[
            { required: true, message: '运单号不能为空' },
            { type: 'number', message: '运单号必须为数字值' },
          ]">
          <el-input v-model.number="form.tracking_number"></el-input>
        </el-form-item>
        <el-form-item label="开始时间" prop='start_time'
        :rules="[
            { required: true, message: '开始时间不能为空' },
          ]">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            value-format="yyyy-MM-dd"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            value-format="yyyy-MM-dd"
            clearable
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="运输状态" prop="status"
        :rules="[
            { required: true, message: '运输状态不能为空' },
          ]">
          <el-radio-group v-model="form.status">
            <el-radio label="completed">已完成</el-radio>
            <el-radio label="in_progress">进行中</el-radio>
          </el-radio-group>
        </el-form-item>
      </template>

      <!-- 销售交易的表单项 -->
      <template v-if="form.type === 'sale'">
        <el-form-item label="产品ID" prop="product_id"
        :rules="[
            { required: true, message: '产品ID不能为空' },
            { type: 'number', message: '产品ID必须为数字值' },
          ]">
          <el-input v-model.number="form.product_id"></el-input>
        </el-form-item>
        <el-form-item label="卖家" prop="seller"
        :rules="[
            { required: true, message: '卖家不能为空' },
          ]">
          <el-input v-model="form.seller"></el-input>
        </el-form-item>
        <el-form-item label="买家" prop="buyer"
        :rules="[
            { required: true, message: '买家不能为空' },
          ]">
          <el-input v-model="form.buyer"></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="price"
        :rules="[
            { required: true, message: '价格不能为空' },
            { type: 'number', message: '价格必须为数字' },
          ]">
          <el-input v-model.number="form.price"></el-input>
        </el-form-item>
      </template>

      <!-- 销售交易的表单项 -->
      <template v-if="form.type === 'sale'">
        <!-- 类似地添加销售交易所需的表单项 -->
      </template>

      <el-form-item>
        <el-button type="primary" @click="submitForm('form')">提交</el-button>
        <el-button @click="resetForm('form')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { addTransaction } from "@/api/blockchain"; // 确保路径匹配您的项目结构
export default {
  data() {
    return {
      form: {
        type: "production", // 交易类型
        status: "completed", // 物流交易状态
        // 在这里初始化其他所有可能的字段
      },
    };
  },
  watch: {},
  methods: {
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    onChangeType(formName) {
      // // 保存当前选择的交易类型
      // const currentType = this.form.type;

      // // 重置表单
      // this.$refs[formName].resetFields();
    },
    getCurrentTimestamp() {
      var now = new Date();
      var year = now.getFullYear();
      var month = String(now.getMonth() + 1).padStart(2, "0"); // 月份是从0开始的
      var day = String(now.getDate()).padStart(2, "0");
      var hours = String(now.getHours()).padStart(2, "0");
      var minutes = String(now.getMinutes()).padStart(2, "0");
      var seconds = String(now.getSeconds()).padStart(2, "0");

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    submitForm(formName) {
      // 在这里实现表单提交的逻辑，如API调用
      // 使用this.form.type来判断提交哪种类型的交易，并根据类型收集相应的表单数据
      this.$refs[formName].validate((valid) => {
        console.log("dwd", valid);
        if (valid) {
          // 根据form.type调用不同的API
          console.log("提交数据", this.form);
          // 构建请求数据
          const requestData = {
            type: this.form.type, // 交易类型
            // 提交时自动生成timestamp
            timestamp: this.getCurrentTimestamp(),
            product_id: this.form.product_id,
            // 根据不同的交易类型，可能需要添加的其他字段
            ...(this.form.type === "production" && {
              batch_number: this.form.batch_number,
              production_date: this.form.production_date,
              factory: this.form.factory,
              origin_place: this.form.origin_place,
            }),
            ...(this.form.type === "logistics" && {
              from_address: this.form.from_address,
              to_address: this.form.to_address,
              carrier: this.form.carrier,
              tracking_number: this.form.tracking_number,
              start_time: this.form.start_time,
              end_time: this.form.end_time,
              status: this.form.status,
            }),
            ...(this.form.type === "sale" && {
              seller: this.form.seller,
              buyer: this.form.buyer,
              price: this.form.price,
            }),
          };
          addTransaction(requestData).then((response) => {
            this.$message.success(response.message);
          });
          console.log("请求数据", requestData);
        } else {
          console.log("表单验证失败");
          return false;
        }
      });
    },
  },
};
</script>

<style scoped>
p {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
</style>
