import { homeworkName } from "./mutation"

export const setinfo = ({ commit }, info) => {
    commit("info", info)
}
export const setHomeworkName = ({ commit }, homeworkName) => {
    commit("homeworkName", homeworkName)
}