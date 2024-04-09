<!--
 * @Description: 
 * @Author: lyq
 * @Date: 2021-11-19 15:21:54
 * @LastEditTime: 2024-04-06 00:06:33
 * @LastEditors: lyq
-->
<template>
  <div class="dashboard-container">
    <p>选择节点</p>
    <el-select
      v-model="current_node"
      filterable
      placeholder="请选择当前节点"
      @change="changeCurrentNode(current_node)"
    >
      <el-option
        v-for="item in node_option"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
    <el-button type="primary" style="margin-left: 1vw" @click="resolve()"
      >区块链同步</el-button>
    <!-- <br /> -->
    <p>注册新节点</p>
    <el-select
      v-model="newNodes"
      multiple
      filterable
      allow-create
      default-first-option
      placeholder="请输入要注册的节点"
    >
    </el-select>
    <el-button
      type="primary"
      style="margin-top: 2vh; margin-left: 1vw"
      @click="registerNewNode()"
      >注册节点</el-button
    >
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { resolveChain, registerNode } from "@/api/blockchain";
export default {
  name: "Dashboard",
  computed: {
    ...mapGetters(["name"]),
  },
  methods: {
    validateNodeUrls(nodeUrls) {
      // 正则表达式匹配以http://或https://开头的URL
      const pattern = /^(http:\/\/|https:\/\/).+/;
      return nodeUrls.every((url) => pattern.test(url));
    },
    changeCurrentNode(value) {
      this.$globalVariables.currentNode = value;
    },
    resolve() {
      resolveChain().then((res) => {
        this.$message({
          message: res.message,
          type: "success",
        });
      });
    },
    registerNewNode() {
      console.log(this.newNodes);
      if (this.validateNodeUrls(this.newNodes)) {
        registerNode({"nodes":this.newNodes}).then((res) => {
          this.$globalVariables.nodeList =
            this.$globalVariables.nodeList.concat(this.newNodes);
          this.$message({
            message: "节点注册成功",
            type: "success",
          });
        });
      } else {
        this.$message({
          message: "节点注册失败，请检查URL格式",
          type: "error",
        });
      }
    },
  },
  data() {
    return {
      node_option: this.$globalVariables.nodeList,
      current_node: this.$globalVariables.currentNode,
      newNodes: [],
    };
  },
  created() {},
  // methods:{
  //   changeCurrentNode(value){
  //     process.env.VUE_APP_CURRENT_NODE = value
  //   }
  // }
};
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin-left: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
