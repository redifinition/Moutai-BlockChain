<template>
  <div class="app-container">
    <el-button
      type="primary"
      icon="el-icon-zoom-in"
      style="margin-bottom: 5vh"
      @click="openConfirm"
      >新增区块</el-button
    >
    <el-table
      v-loading="listLoading"
      :data="blockChain"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column prop="index" align="center" width="65" label="索引">
      </el-table-column>
      <el-table-column prop="timestamp" label="时间戳"> </el-table-column>
      <el-table-column prop="hash" label="哈希值"> </el-table-column>
      <el-table-column prop="previous_hash" label="前一区块的哈希值">
      </el-table-column>

      <el-table-column prop="lenTransaction" label="交易数"> </el-table-column>
      <el-table-column label="交易记录" width="120">
        <template slot-scope="scope">
          <el-button
            type="text"
            size="small"
            @click="handleClick(scope.row.index)"
          >
            查看
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible">
      <!-- {{ this.blockChain[this.currentBlockNum-1].transactions }} -->
      <el-collapse v-model="activeNames" >
        <el-collapse-item
          v-for="(transaction, index) in transactions"
          :key="index"
          :title="'交易'+(index+1) "
          :name="index"
        >
          <div>
            交易ID：{{transaction.transaction_id}}
          </div>
          <div>
            交易类型：{{type[transaction.type]}}
          </div>
          <div>
            时间戳：{{transaction.timestamp}}
          </div>
          <div>
            产品ID：{{transaction.product_id}}
          </div>
          <div v-if="transaction.type=='production'">
            <div>
            批次号：{{transaction.details.batch_number}}
          </div>
          <div>
            生产日期：{{transaction.details.production_date}}
          </div>
          <div>
            工厂：{{transaction.details.factory}}
          </div>
          <div>
            原料产地：{{transaction.details.origin_place}}
          </div>
          </div>
          <div v-if="transaction.type == 'logistics'">
            <div>
            发货地址：{{transaction.details.from_address}}
          </div>
          <div>
            收货地址：{{transaction.details.to_address}}
          </div>
          <div>
            运输公司：{{transaction.details.carrier}}
          </div>
          <div>
            运单号：{{transaction.details.tracking_number}}
          </div>
          <div>
            开始时间：{{transaction.details.start_time}}
          </div>
          <div>
            结束时间：{{transaction.details.end_time}}
          </div>
          <div>
            运输状态：{{transaction.details.status}}
          </div>
          </div>
          <div v-if="transaction.type=='sale'">
            <div>
            卖家：{{transaction.details.seller}}
          </div>
          <div>
            买家：{{transaction.details.buyer}}
          </div>
          <div>
            成交价格：{{transaction.details.price}}
          </div>
          </div>
        </el-collapse-item>
        
      </el-collapse>
      <h2 v-if="transactions == null || transactions.length == 0">无数据</h2>
    </el-dialog>
  </div>
</template>

<script>
import { getList } from "@/api/table";
import { getBlockChain, addBlock } from "@/api/blockchain";
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: "success",
        draft: "gray",
        deleted: "danger",
      };
      return statusMap[status];
    },
  },
  computed: {
    // 计算属性用于生成带有变量和文字的标题
    dialogTitle() {
      return `区块索引为${this.currentBlockNum}的交易信息`;
    },
  },
  data() {
    return {
      list: null,
      listLoading: true,
      blockChain: null,
      dialogVisible: false, //对话框
      currentBlockNum: null,
      transactions: null,
      activeNames:[1],
      type : {
        'production': '生产交易',
        'logistics': '物流交易',
        'sale': '销售交易'
      }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    handleClick(rowNum) {
      console.log("dwd", rowNum);
      this.currentBlockNum = rowNum;
      this.dialogVisible = true;
      this.transactions = this.blockChain[rowNum - 1].transactions;
    },
    openConfirm() {
      this.$confirm("此操作将新增区块, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.listLoading = true;
          addBlock().then((response) => {
            this.listLoading = false;
            this.fetchData();
          });
          this.$message({
            type: "success",
            message: "成功新增一个区块!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消",
          });
        });
    },
    fetchData() {
      this.listLoading = true;
      getBlockChain().then((response) => {
        console.log(response.chain[0].transactions.length);
        this.listLoading = false;
        this.blockChain = response.chain;
        for (let i = 0; i < this.blockChain.length; i++) {
          this.blockChain[i].lenTransaction =
            response.chain[i].transactions.length;
        }
        console.log(this.blockChain);
      });
    },
  },
};
</script>
