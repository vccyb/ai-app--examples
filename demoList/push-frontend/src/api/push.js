import request from './request'

/**
 * 推送相关API
 */
export default {
  /**
   * 预览推送内容
   */
  preview(data) {
    return request({
      url: '/api/push/preview',
      method: 'post',
      data
    })
  },

  /**
   * 执行推送
   */
  execute(data) {
    return request({
      url: '/api/push/execute',
      method: 'post',
      data
    })
  }
}
