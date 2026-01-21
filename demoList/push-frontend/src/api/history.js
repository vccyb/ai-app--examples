import request from './request'

/**
 * 推送历史相关API
 */
export default {
  /**
   * 分页查询历史记录
   */
  getPage(page = 0, size = 10) {
    return request({
      url: '/api/push/history/page',
      method: 'get',
      params: { page, size }
    })
  },

  /**
   * 获取详情
   */
  getById(id) {
    return request({
      url: `/api/push/history/${id}`,
      method: 'get'
    })
  }
}
