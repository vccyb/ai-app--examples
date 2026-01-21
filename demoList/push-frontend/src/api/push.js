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
  },

  /**
   * 获取所有推送平台
   */
  getPlatforms() {
    return request({
      url: '/api/push/platforms',
      method: 'get'
    })
  }
}
