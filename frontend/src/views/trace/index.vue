<!--
 * @Description: 
 * @Author: lyq
 * @Date: 2021-11-19 15:21:54
 * @LastEditTime: 2024-04-08 14:46:11
 * @LastEditors: lyq
-->
<template>
  <div class="app-container">
    <el-input
      v-model="productId"
      placeholder="请输入产品ID"
      class="input-with-select"
      style="width: 50%;"
    >
      <el-button
        slot="append"
        icon="el-icon-search"
        @click="fetchProductTrace"
      ></el-button>
    </el-input>

    <el-table :data="traceData" style="width: 90%; margin-top: 1vh;" border>
      <el-table-column prop="timestamp" label="时间戳" width="180">
      </el-table-column>
      <el-table-column prop="product_id" label="产品ID" width="180">
      </el-table-column>
      <el-table-column prop="transaction_id" label="交易ID" width="250">
      </el-table-column>
      <el-table-column
        label="交易类型"
        width="120">
        <template slot-scope="scope">
          {{ translateType(scope.row.type) }}
        </template>
      </el-table-column>
      <el-table-column label="详情" min-width="250">
        <template slot-scope="scope">
          <!-- 动态显示不同交易类型的详情 -->
          <div v-if="scope.row.type === 'logistics'">
            <p><strong>快递公司:</strong> {{ scope.row.details.carrier }}</p>
            <p>
              <strong>追踪号码:</strong> {{ scope.row.details.tracking_number }}
            </p>
            <p><strong>从:</strong> {{ scope.row.details.from_address }}</p>
            <p><strong>到:</strong> {{ scope.row.details.to_address }}</p>
            <p><strong>开始时间:</strong> {{ scope.row.details.start_time }}</p>
            <p><strong>结束时间:</strong> {{ scope.row.details.end_time }}</p>
            <p><strong>状态:</strong> {{ scope.row.details.status }}</p>
          </div>
          <div v-else-if="scope.row.type === 'production'">
            <!-- 生产交易的展示信息 -->
            <p><strong>批次号:</strong> {{ scope.row.details.batch_number }}</p>
            <p>
              <strong>生产日期:</strong> {{ scope.row.details.production_date }}
            </p>
            <p><strong>工厂:</strong> {{ scope.row.details.factory }}</p>
            <p>
              <strong>原料产地:</strong> {{ scope.row.details.origin_place }}
            </p>
          </div>
          <div v-else-if="scope.row.type === 'sale'">
            <!-- 销售交易的展示信息 -->
            <p><strong>卖家:</strong> {{ scope.row.details.seller }}</p>
            <p><strong>买家:</strong> {{ scope.row.details.buyer }}</p>
            <p><strong>价格:</strong> {{ scope.row.details.price }}</p>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {getProductHistory} from "@/api/blockchain";
export default {
  data() {
    return {
      productId: "",
      // 假设这是从API获取的数据
      traceData: [

]
    };
  },
  methods: {
    translateType(type) {
      const typeTranslations = {
        logistics: '物流',
        production: '生产',
        sale: '销售'
      };
      return typeTranslations[type] || '未知类型';
    },
    fetchProductTrace() {
      if (!this.productId) {
        this.$message({
          type: "warning",
          message: "产品ID不能为空",
        });
        return;
      }
      getProductHistory(this.productId).then((res) => {
        this.traceData = res.transactions;
        this.$message.success("获取产品追溯信息成功");
      });
    },
  },
};
</script>

<style scoped>
.line {
  text-align: center;
}
.product-trace p {
  margin: 0;
  padding: 2px 0;
}
</style>

