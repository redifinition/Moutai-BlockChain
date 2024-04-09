/*
 * @Description: 
 * @Author: lyq
 * @Date: 2024-04-01 21:08:46
 * @LastEditTime: 2024-04-08 14:40:40
 * @LastEditors: lyq
 */
import request from '@/utils/request'

/*返回整个区块链*/
export function getBlockChain() {
  return request({
    url: '/chain',
    method: 'get'
  })
}


// 添加新交易
export function addTransaction(data) {
    return request({
      url: '/transactions/new',
      method: 'post',
      data // 这里传递表单数据到后端
    })
  }


// 新增区块
export function addBlock() {
    return request({
      url: '/mine',
      method: 'get',
    })
  }

// 区块链同步
export function resolveChain() {
    return request({
      url: '/nodes/resolve',
      method: 'get',
    })
  }

// 注册节点
export function registerNode(data) {
    return request({
      url: '/nodes/register',
      method: 'post',
      data
    })
  }

//溯源查询
export function getProductHistory(product_id) {
    return request({
      url: `/product/history?product_id=${product_id}`,
      method: 'get'
    });
  }
  